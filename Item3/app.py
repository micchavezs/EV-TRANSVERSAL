from flask import Flask, request, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

BASE_DATOS = "usuarios.db"


def conectar_base_datos():
    """
    Crea y retorna una conexión con la base de datos SQLite.
    """
    conexion = sqlite3.connect(BASE_DATOS)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tabla():
    """
    Crea la tabla usuarios si todavía no existe.
    """
    conexion = conectar_base_datos()

    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )

    conexion.commit()
    conexion.close()


def registrar_usuario(nombre, contraseña):
    """
    Registra un usuario y almacena su contraseña como hash.
    """
    password_hash = generate_password_hash(contraseña)

    conexion = conectar_base_datos()

    try:
        conexion.execute(
            """
            INSERT INTO usuarios (nombre, password_hash)
            VALUES (?, ?)
            """,
            (nombre, password_hash)
        )

        conexion.commit()

    except sqlite3.IntegrityError:
        # El usuario ya se encuentra registrado.
        pass

    finally:
        conexion.close()


def cargar_integrantes():
    """
    Registra los integrantes iniciales del examen.
    Cambia estos nombres y contraseñas por los reales.
    """
    integrantes = [
        ("Michael", "michael123"),
        ("Juan", "juan123")
    ]

    for nombre, contraseña in integrantes:
        registrar_usuario(nombre, contraseña)


def validar_usuario(nombre, contraseña):
    """
    Valida el nombre y la contraseña ingresados.
    """
    conexion = conectar_base_datos()

    usuario = conexion.execute(
        """
        SELECT nombre, password_hash
        FROM usuarios
        WHERE nombre = ?
        """,
        (nombre,)
    ).fetchone()

    conexion.close()

    if usuario is None:
        return False

    return check_password_hash(
        usuario["password_hash"],
        contraseña
    )


@app.route("/", methods=["GET", "POST"])
def inicio():
    mensaje = ""
    tipo_mensaje = ""

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        contraseña = request.form.get("contraseña", "")

        if not nombre or not contraseña:
            mensaje = "Debe completar el usuario y la contraseña."
            tipo_mensaje = "error"

        elif validar_usuario(nombre, contraseña):
            mensaje = f"Bienvenido, {nombre}. Usuario validado correctamente."
            tipo_mensaje = "correcto"

        else:
            mensaje = "Usuario o contraseña incorrectos."
            tipo_mensaje = "error"

    pagina = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>Validación de usuarios</title>

        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background-color: #eef2f7;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }

            .contenedor {
                background-color: white;
                width: 360px;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
            }

            h1 {
                text-align: center;
                color: #263238;
                margin-bottom: 8px;
            }

            .subtitulo {
                text-align: center;
                color: #607d8b;
                margin-bottom: 25px;
            }

            label {
                display: block;
                margin-top: 14px;
                margin-bottom: 6px;
                font-weight: bold;
            }

            input {
                width: 100%;
                padding: 10px;
                box-sizing: border-box;
                border: 1px solid #b0bec5;
                border-radius: 6px;
            }

            button {
                width: 100%;
                margin-top: 22px;
                padding: 11px;
                border: none;
                border-radius: 6px;
                background-color: #1565c0;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }

            button:hover {
                background-color: #0d47a1;
            }

            .mensaje {
                margin-top: 20px;
                padding: 12px;
                border-radius: 6px;
                text-align: center;
            }

            .correcto {
                background-color: #dff2e1;
                color: #1b5e20;
            }

            .error {
                background-color: #fde0e0;
                color: #b71c1c;
            }
        </style>
    </head>

    <body>
        <div class="contenedor">
            <h1>Inicio de sesión</h1>

            <p class="subtitulo">
                Validación de integrantes
            </p>

            <form method="POST">
                <label for="nombre">Usuario</label>

                <input
                    type="text"
                    id="nombre"
                    name="nombre"
                    required
                >

                <label for="contraseña">Contraseña</label>

                <input
                    type="password"
                    id="contraseña"
                    name="contraseña"
                    required
                >

                <button type="submit">
                    Iniciar sesión
                </button>
            </form>

            {% if mensaje %}
                <div class="mensaje {{ tipo_mensaje }}">
                    {{ mensaje }}
                </div>
            {% endif %}
        </div>
    </body>
    </html>
    """

    return render_template_string(
        pagina,
        mensaje=mensaje,
        tipo_mensaje=tipo_mensaje
    )


if __name__ == "__main__":
    crear_tabla()
    cargar_integrantes()

    print("Aplicación disponible en http://127.0.0.1:5800")

    app.run(
        host="0.0.0.0",
        port=5800,
        debug=False
    )
