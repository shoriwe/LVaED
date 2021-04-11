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

__all__ = ["transformations_blueprint"]

transformations_blueprint = flask.Blueprint("Transformation", "transformation")

kinds = ["Script", "Module", "Class", "Function", "Class Method", "Base", "Argument", "ImportFrom",
         "ImportFromTarget"]


def get_parent(node: dict, links: dict):
	parent = tuple(filter(lambda node_id: node["id"] in links[node_id], links.keys()))[0]
	links[parent].remove(node["id"])
	return parent


class Compiler(object):
	def __init__(self, code_tree: dict):
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

	def compile_import_from(self, node):
		children = []
		while self.cursor < self.number_of_nodes:
			child_node = self.nodes[self.cursor]
			if child_node["kind"] != "ImportFromTarget":
				break
			self.cursor += 1
			children.append(child_node["name"])
		return f"from {node['name']} import " + ", ".join(children)

	def compile_module(self, node):
		return f"import {node['name']}"

	def compile_class(self, node):
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
			class_methods.append(class_method)
		result = f"class {node['name']}"
		if bases:
			result += "(" + ", ".join(bases) + ")"
		result += ":"
		if class_methods:
			for class_method in class_methods:
				result += f"\n\n\tdef {class_method[0]}(" + ", ".join(class_method[1:]) + "):\n\t\tpass"
		else:
			result += "\n\tpass"
		return result

	def compile_function(self, node):
		arguments = []
		while self.cursor < self.number_of_nodes:
			argument = self.nodes[self.cursor]
			if argument["kind"] != "Argument":
				break
			self.cursor += 1
			arguments.append(argument["name"])
		return f"def {node['name']}(" + ", ".join(arguments) + "\n\tpass"

	def compile_code(self) -> str:
		code = ""
		while self.cursor < self.number_of_nodes:
			node = self.nodes[self.cursor]
			self.cursor += 1
			if node["kind"] == "ImportFrom":
				code += self.compile_import_from(node)
			elif node["kind"] == "Module":
				code += self.compile_module(node)
			elif node["kind"] == "Class":
				code += "\n\n" + self.compile_class(node)
			elif node["kind"] == "Function":
				code += "\n\n" + self.compile_function(node)
			else:
				continue
			# print(node["kind"])
			code += "\n"
		return code


class ListObjects(object):
	def __init__(self, raw_code_tree: str):
		code_tree = json.loads(raw_code_tree)
		self.imports = "ID | Source | Names\n ---- | ---- | ----"
		self.updated_imports = False
		self.classes = "ID | Class Name | Bases | Methods\n ----- | ----- | ----- | -----"
		self.updated_classes = False
		self.functions = "ID | Function Name | Arguments\n ----- | ----- | -----"
		self.updated_functions = False
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
		result = ""
		if self.updated_imports:
			result += "## Script imports\n\n\n" + self.imports + "\n\n\n\n"
		if self.updated_classes:
			result += "## Script defined classes\n\n\n" + self.classes + "\n\n\n\n"
		if self.updated_functions:
			result += "## Script defined functions\n\n\n" + self.functions + "\n\n\n\n"
		return result

	def list_objects(self) -> str:
		while self.cursor < self.number_of_nodes:
			node = self.nodes[self.cursor]
			self.cursor += 1
			if node["kind"] == "ImportFrom":
				self.updated_imports = True
				self.describe_import_from(node)
			elif node["kind"] == "Module":
				self.updated_imports = True
				self.describe_module(node)
			elif node["kind"] == "Class":
				self.updated_classes = True
				self.describe_class(node)
			elif node["kind"] == "Function":
				self.updated_functions = True
				self.describe_function(node)
			else:
				continue
		# print(node["kind"])
		return self.generate_code_description()


@transformations_blueprint.route("/transformations", methods=("GET", "POST"))
def transformations():
	graph_data_manager = None
	graph_title = None
	json_graph = None
	source_code = None
	if flask.request.method == "POST":
		success = False
		python_code: werkzeug.datastructures.FileStorage
		python_code = flask.request.files.get("python-code")
		if python_code is not None:
			# ToDo: Do something to parse the input file
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
							node_id += 1
							for base in node.bases:
								graph_data_manager.add_node(node_id, name=base.id, kind="Base")
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
					source_code = content
					json_graph = json.dumps(networkx.readwrite.node_link_data(graph_data_manager))
					graph_title = python_code.filename
					success = True
			except (SyntaxError, ValueError, Exception):
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
					source_code = Compiler(raw_graph_data).compile_code()
					graph_title = raw_graph_data["nodes"][0]["name"]
					json_graph = json.dumps(raw_graph_data)
					success = True
				except (json.JSONDecodeError, Exception):
					pass
		if success:
			network_graph = from_networkx(graph_data_manager, networkx.spring_layout, scale=100, center=(0, 0))
			network_graph.node_renderer.glyph = bokeh.models.Circle(size=15,
			                                                        fill_color=bokeh.transform.factor_cmap(
				                                                        "kind",
				                                                        bokeh.palettes.Category20[20],
				                                                        factors=kinds)
			                                                        )

			network_graph.edge_renderer.glyph = bokeh.models.MultiLine(
				line_alpha=0.5,
				line_width=1,
				line_join='miter',
			)
			plot = bokeh.plotting.figure(tooltips=[("Object Name", "@name"), ("Kind", "@kind")],
			                             tools="pan,wheel_zoom,save,reset",
			                             x_range=bokeh.models.Range1d(-150, 150),
			                             y_range=bokeh.models.Range1d(-150, 150),
			                             title=graph_title)
			plot.renderers.append(network_graph)
			script, div = bokeh.embed.components(plot)
			return flask.render_template(
				"basic/page.html",
				page_name="Transformations",
				body_page="transformations/analyser.html",
				listed_objects=markdown.markdown(ListObjects(json_graph).list_objects(),
				                                 extensions=["codehilite", "extra"]),
				metalanguage_source_code=markdown.markdown(
					"# Metalanguage\n\nGenerated metalanguage useful for sharing the graph or regenerate a code "
					f"interface for future use. The metalanguage was stored in the JSON bellow.\n\n\t:::json\n\t{json_graph}"
					"\n\n# Source Code\n\n\t:::python\n\t" + source_code.replace("\n", "\n\t"),
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
