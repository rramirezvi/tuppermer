from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import ClienteForm
from .carrito import Cart
from django.shortcuts import render, get_object_or_404, redirect

from .models import Producto, Categoria, Cientes
# Create your views here.
"""VISTAS PARA EL CATALGO DE PRODUCTOS"""


def index(request):
    listaProductos = Producto.objects.all()
    listaCategorias = Categoria.objects.all()
    context = {'productos': listaProductos, 'categorias': listaCategorias}
    return render(request, 'index.html', context)


def productos_por_categoria(request, categoria_id):
    # Se obtiene la categoria por su id
    objCategoria = Categoria.objects.get(pk=categoria_id)
    # Se obtienen los productos de la categoria
    listaProductos = objCategoria.producto_set.all()

    listaCategorias = Categoria.objects.all()  # Se obtienen todas las categorias

    context = {'productos': listaProductos,
               'categorias': listaCategorias}  # Se crea el contexto

    return render(request, 'index.html', context)


def productosPorNombre(request):
    nombre = request.POST['nombre']

    listaProductos = Producto.objects.filter(nombre__contains=nombre)
    listaCategorias = Categoria.objects.all()
    context = {'productos': listaProductos, 'categorias': listaCategorias}
    return render(request, 'index.html', context)


def productoDetalle(request, producto_id):

    # objproducto = Producto.objects.get(pk=producto_id)
    objeProducto = get_object_or_404(Producto, pk=producto_id)

    context = {'producto': objeProducto}
    return render(request, 'producto.html', context)


"""VISTAS PARA EL CARRITO DE COMPRAS"""


def carrito(request):
    return render(request, 'carrito.html')


def agregarCarrito(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1

    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.add(objProducto, cantidad)

    if request.method == 'GET':
        return redirect('/')

    return render(request, 'carrito.html')


def eliminarProductoCarrito(request, producto_id):
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.delete(objProducto)

    return render(request, 'carrito.html')


def limpiarCarrito(request):
    carritoProducto = Cart(request)
    carritoProducto.clear()

    return render(request, 'carrito.html')


"""VISTAS PARA CLIENTES Y USURIOS"""


def crearUsuario(request):
    if request.method == 'POST':
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']

        if User.objects.filter(username=dataUsuario).exists():
            return render(request, 'login.html', {'mensaje': 'Usuario ya existe'})
        else:
            nuevoUsuario = User.objects.create_user(
                username=dataUsuario, password=dataPassword)
            if nuevoUsuario is not None:
                login(request, nuevoUsuario)
                return redirect('/cuenta/')

    return render(request, 'login.html')


def loginUsuario(request):
    paginaDestino = request.GET.get('next', None)
    context = {
        'destino': paginaDestino,
    }
    if request.method == 'POST':
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']

        usuarioAuth = authenticate(
            request, username=dataUsuario, password=dataPassword)
        if usuarioAuth is not None:
            login(request, usuarioAuth)

            if dataDestino != '':
                return redirect(dataDestino)

            return redirect('/cuenta')

        else:
            context = {'mensaje': 'Usuario o contraseña incorrectos'}

    return render(request, 'login.html', context)


def logoutUsuario(request):
    logout(request)
    return render(request, 'login.html')


def cuentaUsuario(request):

    try:
        clienteEditar = Cientes.objects.get(usuario=request.user)

        dataCliente = {'nombre': request.user.first_name,
                       'apellido': request.user.last_name,
                       'email': request.user.email,
                       'direccion': clienteEditar.direccion,
                       'telefono': clienteEditar.telefono,
                       'cedula': clienteEditar.cedula,
                       'sexo': clienteEditar.sexo,
                       'fecha_nacimiento': clienteEditar.fecha_nacimiento
                       }
    except:
        dataCliente = {'nombre': request.user.first_name,
                       'apellido': request.user.last_name,
                       'email': request.user.email, }

    frmCliente = ClienteForm(dataCliente)
    context = {'frmCliente': frmCliente}
    return render(request, 'cuenta.html', context)


def actualizarCliente(request):
    mensaje = ""
    if request.method == 'POST':
        frmCliente = ClienteForm(request.POST)
        if frmCliente.is_valid():
            dataCliente = frmCliente.cleaned_data

            # actualizar el usuario
            actUsuario = User.objects.get(pk=request.user.id)
            # campos que vienen del formulario
            actUsuario.first_name = dataCliente['nombre']
            actUsuario.last_name = dataCliente['apellido']
            actUsuario.email = dataCliente['email']
            actUsuario.save()

            # registrar o actualizar al cliente
            if Cientes.objects.filter(usuario=actUsuario).exists():
                actCliente = Cientes.objects.get(usuario=actUsuario)
                actCliente.cedula = dataCliente['cedula']
                actCliente.sexo = dataCliente['sexo']
                actCliente.fecha_nacimiento = dataCliente['fecha_nacimiento']
                actCliente.telefono = dataCliente['telefono']
                actCliente.direccion = dataCliente['direccion']
                actCliente.save()

            else:
                nuevoCLiente = Cientes()
                nuevoCLiente.usuario = actUsuario
                nuevoCLiente.cedula = dataCliente['cedula']
                nuevoCLiente.sexo = dataCliente['sexo']
                nuevoCLiente.fecha_nacimiento = dataCliente['fecha_nacimiento']
                nuevoCLiente.telefono = dataCliente['telefono']
                nuevoCLiente.direccion = dataCliente['direccion']
                nuevoCLiente.save()

            mensaje = "Datos actualizados correctamente"

    else:
        frmCliente = ClienteForm()

    context = {'frmCliente': frmCliente, 'mensaje': mensaje}
    return render(request, 'cuenta.html', context)


"""VISTAS PARA EL PROCESO DE COMPRA"""


# decorador para verificar que el usuario este logueado
@login_required(login_url='/login/')
def registrarPedido(request):

    try:
        clienteEditar = Cientes.objects.get(usuario=request.user)

        dataCliente = {'nombre': request.user.first_name,
                       'apellido': request.user.last_name,
                       'email': request.user.email,
                       'direccion': clienteEditar.direccion,
                       'telefono': clienteEditar.telefono,
                       'cedula': clienteEditar.cedula,
                       'sexo': clienteEditar.sexo,
                       'fecha_nacimiento': clienteEditar.fecha_nacimiento
                       }
    except:
        dataCliente = {'nombre': request.user.first_name,
                       'apellido': request.user.last_name,
                       'email': request.user.email, }

    frmCliente = ClienteForm(dataCliente)

    context = {'frmCliente': frmCliente}

    return render(request, 'pedido.html', context)
