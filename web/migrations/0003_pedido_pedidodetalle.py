# Generated by Django 3.2 on 2024-04-11 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_cientes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('nro_pedido', models.CharField(max_length=20, null=True)),
                ('fecha_entrega', models.DateTimeField()),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('estado', models.CharField(choices=[('P', 'Pendiente'), ('E', 'Enviado'), ('C', 'Pagado')], default='P', max_length=1)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.cientes')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.producto')),
            ],
        ),
    ]
