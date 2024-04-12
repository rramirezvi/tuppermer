from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('productosPorCategoria/<int:categoria_id>',
         views.productos_por_categoria, name='productos_por_categoria'),
    path('productosPorNombre/', views.productosPorNombre,
         name='productosPorNombre'),
    path('productoDetalle/<int:producto_id>',
         views.productoDetalle, name='productoDetalle'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregarCarrito/<int:producto_id>',
         views.agregarCarrito, name='agregarCarrito'),
    path('eliminarProductoCarrito/<int:producto_id>',
         views.eliminarProductoCarrito, name='eliminarProductoCarrito'),
    path('limpiarCarrito/', views.limpiarCarrito, name='limpiarCarrito'),
    path('crearUsuario/', views.crearUsuario, name='crearUsuario'),
    path('cuenta/', views.cuentaUsuario, name='cuenta'),
    path('actualizarCliente/', views.actualizarCliente, name='actualizarCliente'),
    path('login/', views.loginUsuario, name='loginUsuario'),
]
