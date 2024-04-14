from flask import Blueprint, render_template, redirect, request
from simplesdk.internal import AulaSDK, AulaData, AlphacrmSDK
from os import environ
from dotenv import load_dotenv
from urllib.parse import urlparse
from simplesdk.translations import translation, language

loc = translation(
    environ["ET_TRANSLATIONS"]
    or "https://git.tech.eus/EuskadiTech/Translations/raw/branch/main/SimpleAxel.json"
)

load_dotenv()

app = Blueprint("aula7", __name__, url_prefix="/aula7", template_folder="templates")
client = AulaSDK(environ["ET_USER"], environ["ET_PASSWORD"], environ["ET_BASEURL"])
client2 = AlphacrmSDK(environ["ET_USER"], environ["ET_PASSWORD"], environ["ET_BASEURL"])


def login_session():
    user = client2.login_with_session(request.cookies.get("et_auth_session"))
    return user


def safe_urlparse(target):
    target = target.replace("\\", "")
    if not urlparse(target).netloc:
        return target
    else:
        raise ValueError("Unsafe User Input")


def gen_data():
    aula_code = request.args.get("aula_code")
    obj = {"error": False, "aula": {"exists": True}}
    try:
        if aula_code != "" and aula_code != None:
            aula_code = aula_code.lower()
            ad = AulaData(aula_code, dict(request.args), client)
            obj = ad.run()
        else:
            obj["error"] = "El aula no existe, comprueba el codigo."
            obj["aula"]["exists"] = False
    except StopIteration:
        obj["error"] = "El aula no existe, comprueba el codigo."
        obj["aula"]["exists"] = False
    return obj


def gen_data_slow():
    """Deprecated in favour of the new gen_data that uses AulaData"""
    aula_code = request.args.get("aula_code")
    if aula_code != None:
        aula_code = aula_code.lower()
    obj = {
        "request": {
            "args": dict(request.args),
        },
        "aula": {
            "exists": True,
        },
        "error": "",
        "alumnos": [],
        "tareas": [],
        "comedor": {},
        "comedor_reciente": [],
        "today": client.today(),
        "funcs": [],
    }
    try:
        if aula_code != "" and aula_code != None:
            aula = client.aulas__getByCode(aula_code)["0(aulas)"]
            obj["tareas"] = list(client.tareas__filter(aula["id"]))
            obj["alumnos"] = list(client.alumnos__filter(aula["id"]))
            obj["comedor"] = client.comedor__hoy(aula_code)
            obj["comedor_reciente"] = list(client.comedor__filter(aula_code))
            obj["funcs"] = str(
                aula["funcs"]
            ).split()  # Split by spaces, deleting empty strings.
    except StopIteration:
        obj["error"] = "El aula no existe, comprueba el codigo."
        obj["aula"]["exists"] = False
    return obj


@app.route("/")
def index():
    user = login_session()
    if user == None:
        return render_template(
            "aula7/index.html",
            gd=gen_data(),
            products=[],
            aulas=[],
            __=language(loc, request.cookies.get("lang") or "es"),
        )
    a = [
        aula
        for aula in client.aulas__all()
        if aula["1(clientes)"]["correo"] == user["0(clientes)"]["correo"]
    ]
    return render_template(
        "aula7/index.html",
        gd=gen_data(),
        products=str(user["0(clientes)"]["products"]).split(),
        aulas=a,
        __=language(loc, request.cookies.get("lang") or "es"),
    )


@app.route("/u/index")
def u_index():
    return render_template(
        "aula7/u/index.html",
        gd=gen_data(),
        __=language(loc, request.cookies.get("lang") or "es"),
    )


@app.route("/u/resumen")
def u_resumen():
    return render_template(
        "aula7/u/resumen.html",
        gd=gen_data(),
        __=language(loc, request.cookies.get("lang") or "es"),
    )


@app.route("/u/comedor")
def u_comedor():
    return render_template(
        "aula7/u/comedor.html",
        gd=gen_data(),
        __=language(loc, request.cookies.get("lang") or "es"),
    )


@app.route("/u/data.json")
def u_data_json():
    gd = gen_data()
    gd = dict(gd)
    return gd


@app.route("/u/alumnos")
def u_alumnos():
    return render_template(
        "aula7/u/alumnos.html",
        gd=gen_data(),
        __=language(loc, request.cookies.get("lang") or "es"),
    )


@app.route("/u/alumno_edit")
def u_alumno_edit():
    return render_template(
        "aula7/u/alumno_edit.html",
        gd=gen_data(),
        ta=client.alumnos__get(int(request.args["id"])),
        __=language(loc, request.cookies.get("lang") or "es"),
    )


@app.route("/u/alumno_new")
def u_alumno_new():
    return render_template(
        "aula7/u/alumno_new.html",
        gd=gen_data(),
        __=language(loc, request.cookies.get("lang") or "es"),
    )


@app.route("/_/alumnos/new", methods=["POST"])
def api_alumnos_new():
    aula = client.aulas__getByCode(request.args["aula_code"])["0(aulas)"]["id"]
    client.alumnos__new(
        aula,
        request.form["correo"],
        request.form["detalles_alumno"],
        request.form["nombre_alumno"],
        request.form["telefono"],
    )
    gd = gen_data()
    return redirect(
        f'/aula7/u/alumnos?aula_code={safe_urlparse(gd["request"]["args"]["aula_code"])}'
    )


@app.route("/_/alumnos/edit", methods=["POST"])
def api_alumnos_edit():
    aula = client.aulas__getByCode(request.args["aula_code"])["0(aulas)"]["id"]
    client.alumnos__edit(
        int(request.form["id"]),
        aula,
        request.form["correo"],
        request.form["detalles_alumno"],
        request.form["nombre_alumno"],
        request.form["telefono"],
    )
    gd = gen_data()
    return redirect(
        f'/aula7/u/alumnos?aula_code={safe_urlparse(gd["request"]["args"]["aula_code"])}'
    )


@app.route("/_/alumnos/delete")
def api_alumnos_delete():
    client.alumnos__delete(int(request.args["id"]))
    gd = gen_data()
    return redirect(
        f'/aula7/u/alumnos?aula_code={safe_urlparse(gd["request"]["args"]["aula_code"])}'
    )


@app.route("/u/tareas")
def u_tareas():
    return render_template(
        "aula7/u/tareas.html",
        gd=gen_data(),
        __=language(loc, request.cookies.get("lang") or "es"),
    )


@app.route("/u/tarea_edit")
def u_tarea_edit():
    return render_template(
        "aula7/u/tarea_edit.html",
        gd=gen_data(),
        ta=client.tareas__get(int(request.args["id"])),
        __=language(loc, request.cookies.get("lang") or "es"),
    )


@app.route("/u/tarea_new")
def u_tarea_new():
    return render_template(
        "aula7/u/tarea_new.html",
        gd=gen_data(),
        __=language(loc, request.cookies.get("lang") or "es"),
    )


@app.route("/_/tareas/new", methods=["POST"])
def api_tareas_new():
    aula = client.aulas__getByCode(request.args["aula_code"])["0(aulas)"]["id"]
    client.tareas__new(
        aula,
        request.form["alumno"],
        request.form["tarea"],
        request.form["fecha_tarea"],
        request.form["orden_tarea"],
    )
    gd = gen_data()
    return redirect(
        f'/aula7/u/tareas?aula_code={safe_urlparse(gd["request"]["args"]["aula_code"])}'
    )


@app.route("/_/tareas/edit", methods=["POST"])
def api_tareas_edit():
    aula = client.aulas__getByCode(request.args["aula_code"])["0(aulas)"]["id"]
    client.tareas__edit(
        int(request.form["id"]),
        aula,
        request.form["alumno"],
        request.form["tarea"],
        request.form["fecha_tarea"],
        request.form["orden_tarea"],
    )
    gd = gen_data()
    return redirect(
        f'/aula7/u/tareas?aula_code={safe_urlparse(gd["request"]["args"]["aula_code"])}'
    )


@app.route("/_/tareas/delete")
def api_tareas_delete():
    client.tareas__delete(int(request.args["id"]))
    gd = gen_data()
    return redirect(
        f'/aula7/u/tareas?aula_code={safe_urlparse(gd["request"]["args"]["aula_code"])}'
    )
