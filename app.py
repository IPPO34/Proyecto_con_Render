from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

tipos_cartera = [
    (1, 'ANDINO'),
    (2, 'TRADICIONAL'),
    (3, 'SELVATICO'),
    (4, 'COSTEÑO')
]

usuarios = [
    {'id': 1, 'nombre': 'carlos', 'contrasena': '123'}
]

carteras = []
contador_cartera = 1 

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/Login', methods=['GET', 'POST'])
def login():
    mensaje = ""
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        for usuario in usuarios:
            if usuario['nombre'] == nombre and usuario['contrasena'] == contrasena:
                return redirect(url_for('principal'))
        mensaje = "Usuario o contraseña incorrectos"
    return render_template("Login.html", mensaje=mensaje)

@app.route('/Principal')
def principal():
    return render_template("Principal.html")

@app.route('/RegistrarCartera')
def form_registro():
    return render_template("RegistrarCartera.html", tipos=tipos_cartera)

@app.route('/GrabarCartera', methods=['POST'])
def grabar():
    global contador_cartera
    nombre = request.form['nombre']
    precio = request.form['precio']
    fecha = request.form['fecha']
    tipo = int(request.form['tipo'])

    cartera = {
        'codcar': contador_cartera,
        'descripcar': nombre,
        'preciocar': precio,
        'fechacar': fecha,
        'codtipcar': tipo
    }
    carteras.append(cartera)
    contador_cartera += 1

    return render_template("RegistrarCartera.html", tipos=tipos_cartera, mensaje="Se grabó el registro satisfactoriamente.")

@app.route('/ConsultarCartera')
def consultar():
    tipo = request.args.get('tipo')
    resultados = []

    if tipo:
        tipo = int(tipo)
        for c in carteras:
            if c['codtipcar'] == tipo:
                nombre_tipo = next((t[1] for t in tipos_cartera if t[0] == tipo), "Desconocido")
                resultados.append((
                    c['codcar'],
                    c['descripcar'],
                    c['preciocar'],
                    c['fechacar'],
                    nombre_tipo
                ))

    return render_template("ConsultarCartera.html", tipos=tipos_cartera, resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
