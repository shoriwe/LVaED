import ast
import io
import json

import bokeh.embed
import bokeh.models
import bokeh.palettes
import bokeh.resources
import bokeh.transform
import flask
import markdown
import networkx
import networkx.readwrite.json_graph
import werkzeug.datastructures
from bokeh.plotting import from_networkx


class ClassDef(object):
	def __init__(self, name, bases, functions):
		self.name = name
		self.bases = bases
		self.functions = functions


class FunctionDef(object):
	def __init__(self, name, arguments):
		self.name = name
		self.arguments = arguments


class Import(object):
	def __init__(self, source, names):
		self.source = source
		self.names = names


__all__ = ["transformations_blueprint"]

transformations_blueprint = flask.Blueprint("Transformation", "transformation")

kinds = [
	"Script", "Module", "Class", "Function", "Class Method", "Base", "Argument", "ImportFrom", "ImportFromTarget"
]


def get_parent(node: dict, links: dict):
	parent = tuple(filter(lambda node_id: node["id"] in links[node_id], links.keys()))[0]
	links[parent].remove(node["id"])
	return parent


class Compiler(object):
	def __init__(self, code_tree: dict or str):
		if isinstance(code_tree, dict):
			self.code_tree = code_tree
		elif isinstance(code_tree, str):
			self.code_tree = json.loads(code_tree)
		else:
			raise TypeError("code_tree must be dict or str")
		self.nodes = self.code_tree["nodes"].copy()
		self.cursor = 1
		self.number_of_nodes = len(self.nodes)
		self.nodes.sort(key=lambda node: node["id"])
		self.links = {}
		for raw_link in map(lambda link: (link["source"], link["target"]), self.code_tree["links"]):
			if raw_link[0] not in self.links.keys():
				self.links[raw_link[0]] = [raw_link[1]]
			else:
				self.links[raw_link[0]].append(raw_link[1])

	def prepare_import_from(self, node) -> Import:
		children = []
		while self.cursor < self.number_of_nodes:
			child_node = self.nodes[self.cursor]
			if child_node["kind"] != "ImportFromTarget":
				break
			self.cursor += 1
			children.append(child_node["name"])
		return Import(node["name"], children)

	def prepare_module(self, node) -> Import:
		return Import(None, [node['name']])

	def prepare_class(self, node) -> ClassDef:
		# Add bases
		bases = []
		while self.cursor < self.number_of_nodes:
			base_node = self.nodes[self.cursor]
			if base_node["kind"] != "Base":
				break
			self.cursor += 1
			bases.append(base_node["name"])
		# Add Class Methods
		class_methods = []
		while self.cursor < self.number_of_nodes:
			class_method_node = self.nodes[self.cursor]
			if class_method_node["kind"] != "Class Method":
				break
			self.cursor += 1
			class_method = [class_method_node["name"]]
			while self.cursor < self.number_of_nodes:
				class_method_argument = self.nodes[self.cursor]
				if class_method_argument["kind"] != "Argument":
					break
				self.cursor += 1
				class_method.append(class_method_argument["name"])
			class_methods.append(FunctionDef(class_method[0], class_method[1:]))
		return ClassDef(node["name"], bases, class_methods)

	def prepare_function(self, node) -> FunctionDef:
		arguments = []
		while self.cursor < self.number_of_nodes:
			argument = self.nodes[self.cursor]
			if argument["kind"] != "Argument":
				break
			self.cursor += 1
			arguments.append(argument["name"])
		return FunctionDef(node["name"], arguments)

	def compile_python_import_from(self, import_from: Import) -> str:
		return f"from {import_from.source} import " + ", ".join(import_from.names)

	def compile_python_import(self, module: Import) -> str:
		return "import " + ", ".join(module.names)

	def compile_python_class(self, class_definition: ClassDef) -> str:
		result = f"class {class_definition.name}(" + ", ".join(class_definition.bases) + "):\n\t" + ("\n\t".join(
			self.compile_python_function(function_definition).replace("\n", "\n\t") + "\n" for function_definition in
			class_definition.functions) if class_definition.functions else "pass")
		if result[-1] == "\n":
			return result[:-1]
		return result

	def compile_python_function(self, function_definition: FunctionDef) -> str:
		return f"def {function_definition.name}(" + ", ".join(function_definition.arguments) + "):\n\tpass"

	def compile_c_class(self, class_definition: ClassDef) -> str:
		result = f"typedef struct {class_definition.name} {{\n\t// Fill the attributes of your struct\n}} {class_definition.name};"
		for function_ in class_definition.functions:
			if function_.name == "__init__":
				function_name = f"{class_definition.name}_new"
				return_type = class_definition.name
			else:
				function_name = f"{class_definition.name}_{function_.name}"
				return_type = "void"
			if function_.arguments:
				result += f"\n\n{return_type} *{function_name}(" + f"{class_definition.name} *{function_.arguments[0]}" + (
					", " + ", ".join(f"void *{argument}" for argument in function_.arguments[1:])
					if function_.arguments[1:] else ""
				) + ");"
			else:
				result += f"\n\n{return_type} *{function_name}();"
		return result

	def compile_c_function(self, function_definition: FunctionDef) -> str:
		return f"void *{function_definition.name}(" + ", ".join(
			f"void *{argument}" for argument in function_definition.arguments) + ");"

	def compile_java_class(self, class_definition: ClassDef) -> str:
		result = f"public class {class_definition.name}{{"
		for function_ in class_definition.functions:
			result += "\n\t\t\t"
			if function_.name == "__init__":
				result += f"public {class_definition.name}(" + ", ".join(
					f"Object {argument}" for argument in
					function_.arguments[1:]) + "){\n\t\t\t\t// Prepare your constructor\n\t\t\t}"
			else:
				result += f"public Object {function_.name}(" + ", ".join(
					f"Object {argument}" for argument in function_.arguments[1:]) + "){return null;}"
			result += "\n"
		result += "\n\t}"
		return result

	def compile_java_function(self, function_definition: FunctionDef) -> str:
		return f"public static Object {function_definition.name}(" + ", ".join(
			f"Object {argument}" for argument in function_definition.arguments) + "){return null;}"

	def compile_code(self) -> (str, str, str):
		last_defined = None
		compiled_python = ""
		compiled_java = "public class Program {"
		compiled_c = ""
		while self.cursor < self.number_of_nodes:
			node = self.nodes[self.cursor]
			self.cursor += 1
			if node["kind"] == "ImportFrom":
				if last_defined in (ClassDef, FunctionDef):
					compiled_python += "\n\n"
				last_defined = Import
				import_from = self.prepare_import_from(node)
				compiled_python += self.compile_python_import_from(import_from)
			elif node["kind"] == "Module":
				if last_defined in (ClassDef, FunctionDef):
					compiled_python += "\n\n"
				last_defined = Import
				module = self.prepare_module(node)
				compiled_python += self.compile_python_import(module)
			elif node["kind"] == "Class":
				last_defined = ClassDef
				class_definition = self.prepare_class(node)
				compiled_python += "\n\n" + self.compile_python_class(class_definition)
				compiled_c += "\n" + self.compile_c_class(class_definition)
				compiled_java += "\n\t" + self.compile_java_class(class_definition)
				compiled_java += "\n\n"
				compiled_c += "\n\n"
			elif node["kind"] == "Function":
				last_defined = FunctionDef
				function_definition = self.prepare_function(node)
				compiled_python += "\n\n" + self.compile_python_function(function_definition)
				compiled_c += self.compile_c_function(function_definition)
				compiled_java += "\n\t" + self.compile_java_function(function_definition)
				compiled_java += "\n\n"
				compiled_c += "\n\n"
			else:
				continue
			compiled_python += "\n"
		compiled_java += "}"
		return compiled_c, compiled_java, compiled_python


class DescribeCode(object):
	def __init__(self, raw_code_tree: str):
		code_tree = json.loads(raw_code_tree)
		self.imports = "ID | Source | Names\n ---- | ---- | ----"
		self.updated_imports = False
		self.classes = "ID | Class Name | Bases | Methods\n ----- | ----- | ----- | -----"
		self.updated_classes = False
		self.functions = "ID | Function Name | Arguments\n ----- | ----- | -----"
		self.updated_functions = False
		self.counter = {"imports": 0, "classes": 0, "functions": 0}
		self.code_tree = code_tree
		self.nodes = self.code_tree["nodes"].copy()
		self.cursor = 1
		self.number_of_nodes = len(self.nodes)
		self.nodes.sort(key=lambda node: node["id"])
		self.links = {}
		for raw_link in map(lambda link: (link["source"], link["target"]), self.code_tree["links"]):
			if raw_link[0] not in self.links.keys():
				self.links[raw_link[0]] = [raw_link[1]]
			else:
				self.links[raw_link[0]].append(raw_link[1])

	def describe_import_from(self, node: dict):
		names = []
		while self.cursor < self.number_of_nodes:
			import_name = self.nodes[self.cursor]
			if import_name["kind"] != "ImportFromTarget":
				break
			self.cursor += 1
			names.append(import_name["name"].replace("_", "\\_"))
			self.counter["imports"] += 1
		name = node['name'].replace("_", "\\_")
		self.imports += f"\n{node['id']} | {name} | " + ", ".join(names)

	def describe_module(self, node: dict):
		name = node['name'].replace("_", "\\_")
		self.imports += f"\n{node['id']} | - | {name}"

	def describe_class(self, node: dict):
		# Add bases
		bases = []
		while self.cursor < self.number_of_nodes:
			base_node = self.nodes[self.cursor]
			if base_node["kind"] != "Base":
				break
			self.cursor += 1
			bases.append(base_node["name"].replace("_", "\\_"))
		# Add Class Methods
		class_methods = []
		while self.cursor < self.number_of_nodes:
			class_method_node = self.nodes[self.cursor]
			if class_method_node["kind"] != "Class Method":
				break
			self.cursor += 1
			class_method = [class_method_node["name"].replace("_", "\\_")]
			while self.cursor < self.number_of_nodes:
				class_method_argument = self.nodes[self.cursor]
				if class_method_argument["kind"] != "Argument":
					break
				self.cursor += 1
				class_method.append(class_method_argument["name"].replace("_", "\\_"))
			class_methods.append(class_method)
		name = node["name"].replace("_", "\\_")
		self.classes += f"\n{node['id']} | {name} | " + "<br> ".join(bases) + " | " + "<br> ".join(
			f"{class_method[0]}\\(" + ", ".join(class_method[1:]) + ")" for class_method in class_methods)

	def describe_function(self, node: dict):
		arguments = []
		while self.cursor < self.number_of_nodes:
			argument = self.nodes[self.cursor]
			if argument["kind"] != "Argument":
				break
			self.cursor += 1
			arguments.append(argument["name"].replace("_", "\\_"))
		name = node['name'].replace("_", "\\_")
		self.functions += f"\n{node['id']} | {name} | " + "<br> ".join(arguments)

	def generate_code_description(self):
		result = "### Amount of objects\n\nKind | Amount\n" + "---- | ----\n" + "\n".join(
			f"{kind.title()} | {self.counter[kind]}" for kind in self.counter.keys()
		) + "\n\n\n\n"
		if self.updated_imports:
			result += "### Script imports\n\n\n" + self.imports + "\n\n\n\n"
		if self.updated_classes:
			result += "### Script defined classes\n\n\n" + self.classes + "\n\n\n\n"
		if self.updated_functions:
			result += "### Script defined functions\n\n\n" + self.functions + "\n\n\n\n"
		return result

	def describe(self) -> str:
		while self.cursor < self.number_of_nodes:
			node = self.nodes[self.cursor]
			self.cursor += 1
			if node["kind"] == "ImportFrom":
				self.updated_imports = True
				self.describe_import_from(node)
			elif node["kind"] == "Module":
				self.counter["imports"] += 1
				self.updated_imports = True
				self.describe_module(node)
			elif node["kind"] == "Class":
				self.counter["classes"] += 1
				self.updated_classes = True
				self.describe_class(node)
			elif node["kind"] == "Function":
				self.counter["functions"] += 1
				self.updated_functions = True
				self.describe_function(node)
			else:
				continue
		# print(node["kind"])
		return self.generate_code_description()


def prepare_source_code(
		compiled_c: str,
		compiled_java: str,
		target_python_code: str,
		generated_python_code: bool) -> str:
	python_title = "Original Python Source Code"
	if generated_python_code:
		python_title = "Generated Python Source Code"
	result = "\n\n# Source Code\n\n"
	if compiled_c:
		result += \
			f"### Generated C Source Code\n\n\t:::c\n\t{compiled_c}\n\n\n" \
			f"### Generated Java Source Code\n\n\t:::java\n\t{compiled_java}\n\n\n"
	else:
		result += \
			f"### Generated C Source Code\n\nThe provided code doesn't have defined any `function` or `class`\n\n\n" \
			f"### Generated Java Source Code\n\nThe provided code doesn't have defined any `function` or `class`\n\n\n"
	return result + f"### {python_title}\n\n\t:::python\n\t{target_python_code}\n\n\n"


@transformations_blueprint.route("/transformations", methods=("GET", "POST"))
def transformations():
	graph_data_manager = None
	graph_title = None
	json_graph = None
	target_python_code = None
	compiled_c = None
	compiled_java = None
	python_code_generated = None
	if flask.request.method == "POST":
		success = False
		python_code: werkzeug.datastructures.FileStorage
		python_code = flask.request.files.get("python-code")
		if python_code is not None:
			buffer = io.BytesIO()
			python_code.save(buffer)
			buffer.seek(0)
			content = buffer.read()
			try:
				content = content.decode()
				parsed_code = ast.parse(content, python_code.filename)
				if parsed_code.body:
					node_id = 1
					graph_data_manager = networkx.Graph()
					graph_data_manager.add_node(node_id, name=python_code.filename, kind="Script")
					node_id += 1
					for node in parsed_code.body:
						if isinstance(node, ast.ImportFrom):
							import_id = node_id
							import_name = ("." * node.level) + node.module
							graph_data_manager.add_node(import_id, name=import_name, kind="ImportFrom")
							graph_data_manager.add_edge(1, import_id, label="From")
							node_id += 1
							for name in node.names:
								graph_data_manager.add_node(node_id, name=name.name, kind="ImportFromTarget")
								graph_data_manager.add_edge(import_id, node_id, label="Import")
								node_id += 1
						elif isinstance(node, ast.Import):
							for name in node.names:
								name: ast.alias
								graph_data_manager.add_node(node_id, name=name.name, kind="Module")
								graph_data_manager.add_edge(1, node_id, label="Imports")
								node_id += 1
						elif isinstance(node, ast.ClassDef):
							class_name = node.name
							class_id = node_id
							graph_data_manager.add_node(class_id, name=class_name, kind="Class")
							graph_data_manager.add_edge(1, class_id, label="Defines")
							found_object_base = False
							node_id += 1
							for base in node.bases:
								if isinstance(base, ast.Attribute):
									parts = []
									while isinstance(base, ast.Attribute):
										parts.append(base.attr)
										base = base.value
									if isinstance(base, ast.Name):
										parts.append(base.id)
									else:
										parts.append("Unknown")
									base_name = ".".join(parts[::-1])
								elif isinstance(base, ast.Name):
									base_name = base.id
								else:
									base_name = "Unknown"
								if base_name == "object":
									found_object_base = True
								graph_data_manager.add_node(node_id, name=base_name, kind="Base")
								graph_data_manager.add_edge(class_id, node_id, label="Implements")
								node_id += 1
							if not found_object_base:
								graph_data_manager.add_node(node_id, name="object", kind="Base")
								graph_data_manager.add_edge(class_id, node_id, label="Implements")
								node_id += 1
							for class_node in node.body:
								if isinstance(class_node, ast.FunctionDef):
									function_id = node_id
									graph_data_manager.add_node(node_id, name=class_node.name, kind="Class Method")
									graph_data_manager.add_edge(class_id, node_id)
									node_id += 1
									for argument in class_node.args.args:
										graph_data_manager.add_node(node_id, name=argument.arg, kind="Argument")
										graph_data_manager.add_edge(function_id, node_id, label="Has")
										node_id += 1
						elif isinstance(node, ast.FunctionDef):
							function_id = node_id
							graph_data_manager.add_node(function_id, name=node.name, kind="Function")
							graph_data_manager.add_edge(1, function_id, label="Defines")
							node_id += 1
							for argument in node.args.args:
								graph_data_manager.add_node(node_id, name=argument.arg, kind="Argument")
								graph_data_manager.add_edge(function_id, node_id, label="Has")
								node_id += 1
					target_python_code = content
					json_graph = json.dumps(networkx.readwrite.node_link_data(graph_data_manager))
					graph_title = python_code.filename
					success = True
					python_code_generated = False
			except (SyntaxError, ValueError, Exception) as e:
				pass
		if not success:
			code_map: werkzeug.datastructures.FileStorage
			code_map = flask.request.files.get("code-map")
			if code_map is not None:
				buffer = io.BytesIO()
				code_map.save(buffer)
				buffer.seek(0)
				content = buffer.read()
				try:
					raw_graph_data = json.loads(content)
					graph_data_manager = networkx.readwrite.json_graph.node_link_graph(raw_graph_data)
					compiled_c, compiled_java, target_python_code = Compiler(raw_graph_data).compile_code()
					graph_title = raw_graph_data["nodes"][0]["name"]
					json_graph = json.dumps(raw_graph_data)
					success = True
					python_code_generated = True
				except (json.JSONDecodeError, Exception) as e:
					pass
		if success:
			network_graph = from_networkx(graph_data_manager, networkx.spring_layout, scale=100, center=(0, 0))
			network_graph.node_renderer.glyph = bokeh.models.Circle(
				size=15,
				fill_color=bokeh.transform.factor_cmap(
					"kind",
					bokeh.palettes.Category20[20],
					factors=kinds
				)
			)

			network_graph.edge_renderer.glyph = bokeh.models.MultiLine(
				line_alpha=0.5,
				line_width=1,
				line_join='miter',
			)
			plot = bokeh.plotting.figure(
				tooltips=[("Object Name", "@name"), ("Kind", "@kind")],
				tools="pan,wheel_zoom,save,reset",
				x_range=bokeh.models.Range1d(-150, 150),
				y_range=bokeh.models.Range1d(-150, 150),
				title=graph_title)
			plot.renderers.append(network_graph)
			script, div = bokeh.embed.components(plot)
			if compiled_c is None and compiled_java is None:
				compiled_c, compiled_java, _ = Compiler(json_graph).compile_code()
			target_python_code = target_python_code.replace("\n", "\n\t")
			compiled_c = compiled_c.replace("\n", "\n\t")
			compiled_java = compiled_java.replace("\n", "\n\t")
			return flask.render_template(
				"basic/page.html",
				page_name="Transformations",
				body_page="transformations/analyser.html",
				listed_objects=markdown.markdown(
					DescribeCode(json_graph).describe(),
					extensions=["codehilite", "extra"]),
				metalanguage=markdown.markdown(
					"# Metalanguage\n\nGenerated metalanguage useful for sharing the graph or regenerate a code "
					f"interface for future use. The metalanguage was stored in the JSON bellow.\n\n\t:::json\n\t{json_graph}",
					extensions=["codehilite", "extra"]),
				source_code=markdown.markdown(
					prepare_source_code(compiled_c, compiled_java, target_python_code, python_code_generated),
					extensions=["codehilite", "extra"]),
				plot_script=script,
				plot_div=div,
				js_resources=bokeh.resources.INLINE.render_js(),
				css_resources=bokeh.resources.INLINE.render_css(),
			)
	return flask.render_template(
		"basic/page.html",
		page_name="Transformations",
		body_page="transformations/file-upload.html"
	)
