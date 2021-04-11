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


def compile_code(code_tree: dict) -> str:
	nodes = code_tree["nodes"].copy()
	nodes.sort(key=lambda n: n["id"])
	code = ""
	in_class_context = False
	in_import_from_context = False
	in_function_context = False
	in_class_method_context = False
	defining_class_bases = False
	for node in nodes[1:]:
		if (not in_class_method_context) and (not defining_class_bases) and in_class_context and \
				(node["kind"] != "Class Method"):
			in_class_method_context = False
			in_class_context = False
			in_function_context = False
			code += "\n\tpass"
		elif in_class_context and defining_class_bases and node["kind"] != "Base":
			if code[-1] == ',':
				code = code[:-1]
			code += "):"
			defining_class_bases = False
		elif in_class_method_context and node["kind"] != "Argument":
			if code[-1] == ',':
				code = code[:-1]
			code += "):\n\t\tpass"
			in_class_method_context = False
			if node["kind"] != "Class Method":
				in_class_context = False
				code += "\n\tpass"
		elif in_function_context and node["kind"] != "Argument":
			if code[-1] == ',':
				code = code[:-1]
			code += "):\n\tpass"
			in_function_context = False
		elif in_import_from_context and node["kind"] != "ImportFromTarget":
			if code[-1] == ',':
				code = code[:-1]
			code += "\n"
			in_import_from_context = False
		if node["kind"] == "Base":
			code += f"{node['name']},"
		elif node["kind"] == "ImportFrom":
			in_import_from_context = True
			code += f"\nfrom {node['name']} import "
		elif node["kind"] == "ImportFromTarget":
			code += f"{node['name']},"
		elif node["kind"] == "Module":
			code += f"\nimport {node['name']}"
		elif node["kind"] == "Class":
			code += f"\n\n\nclass {node['name']}("
			in_class_context = True
			defining_class_bases = True
		elif node["kind"] == "Class Method":
			code += f"\n\n\tdef {node['name']}("
			in_class_method_context = True
		elif node["kind"] == "Function":
			in_function_context = True
			code += f"\n\n\ndef {node['name']}("
		elif node["kind"] == "Argument":
			code += f"{node['name']},"
	if in_function_context:
		if code[-1] == ',':
			code = code[:-1]
		code += "):\n\tpass"
	if in_class_method_context:
		if code[-1] == ',':
			code = code[:-1]
		code += "):\n\t\tpass"
	if in_class_context:
		code += "\n\tpass"
	return code


def list_objects(raw_json_graph: str) -> str:
	result = ""
	try:
		json_graph = json.loads(raw_json_graph)
		for node in json_graph["nodes"]:
			result += node["kind"] + "|" + node["name"].replace("_", "\\_") + "\n"
	except Exception:
		pass
	return result


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
					source_code = compile_code(raw_graph_data)
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
			listed_objects = list_objects(json_graph)
			return flask.render_template(
				"basic/page.html",
				page_name="Transformations",
				body_page="transformations/analyser.html",
				listed_objects=markdown.markdown(
					"Name | Metalanguage Kind | AST Kind \n"
					"---- | ---- | ----\n" + listed_objects + "\n",
					extensions=["codehilite", "tables"]),
				metalanguage_source_code=markdown.markdown(
					"# Metalanguage\n\nGenerated metalanguage useful for sharing the graph or regenerate a code "
					f"interface for future use. The metalanguage was stored in the JSON bellow.\n\n\t:::json\n\t{json_graph}"
					"\n\n# Source Code\n\n\t:::python\n\t" + source_code.replace("\n", "\n\t"),
					extensions=["codehilite"]),
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
