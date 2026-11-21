# The Copper Lantern Hotel

## Objetivo

Desarrollar un sitio informativo y comercial para un hotel boutique ficticio con estética estadounidense clásica. El proyecto se construye con Django y MariaDB e integra un sitio público con un panel administrativo.

La fecha de entrega indicada en la guía académica es el 28 de septiembre de 2026.

## Alcance exigido por la guía

- Logotipo y nombre de la empresa.
- Home con identidad corporativa.
- Servicios dinámicos administrados mediante CRUD.
- Productos dinámicos administrados mediante CRUD. En este proyecto, los productos son las habitaciones.
- Página de contacto.
- Botón de ingreso al aplicativo administrativo.
- Menú, carrusel y pie de página.
- Imágenes para servicios y habitaciones.
- Autenticación administrativa.
- Base de datos MariaDB o MySQL.
- Validaciones de formularios y datos.
- Mensajes de guardado y error.
- Aplicativo integrado orientado al proceso de ventas.

## Identidad del hotel

- Nombre: The Copper Lantern Hotel.
- Concepto: hotel boutique de inspiración estadounidense, antiguo, elegante y acogedor.
- Materiales visuales: nogal oscuro, cuero, latón, vidrio texturizado y luz cálida.
- Símbolos: linterna, llave antigua, placa de habitación y monograma CL.
- Paleta principal:
  - nogal oscuro: `#321F18`;
  - madera: `#62412F`;
  - latón: `#B58A4A`;
  - crema: `#F1E6D2`;
  - verde bosque: `#20372F`;
  - borgoña: `#5A2428`;
  - carbón: `#171513`.

## Sitio público

### Home

- Navbar fijo con logotipo, navegación y acceso administrativo.
- Carrusel con fachada, entrada, lobby y espacios interiores.
- Presentación e historia ficticia del hotel.
- Habitaciones y servicios destacados obtenidos desde la base de datos.
- Indicadores generales del hotel.
- Citas verificadas sobre viajes y hospitalidad.
- Llamado a explorar habitaciones o solicitar una reserva.

### Habitaciones

Cada habitación se representa como una puerta con placa numérica. La interacción depende de su estado:

- `available`: la puerta se abre al pasar el cursor y el clic muestra el detalle.
- `unavailable`: la puerta permanece cerrada y muestra una placa de no disponible.
- `coming_soon`: la puerta permanece cerrada y presenta cintas de construcción.
- `maintenance`: la puerta permanece cerrada y presenta una señal de mantenimiento.

El detalle se muestra en un modal con galería, descripción, precio por noche, capacidad, camas, estancia mínima, horario de entrada y salida, beneficios incluidos y acción para solicitar reserva.

En pantallas táctiles, el clic abre directamente el detalle de las habitaciones disponibles. Las animaciones respetan `prefers-reduced-motion`.

### Servicios

Los servicios son dinámicos y pueden venderse por separado o incluirse como beneficio de una habitación. Ejemplos iniciales:

- spa y sala de vapor;
- masajes;
- desayuno americano;
- restaurante y servicio a la habitación;
- catering para eventos;
- salón para reuniones;
- té junto a la chimenea;
- lavandería;
- traslado desde el aeropuerto;
- estacionamiento o valet parking;
- preparación romántica.

La suite presidencial tendrá registrados como incluidos todos los servicios aplicables. La relación entre habitación y servicio permite distinguir beneficios incluidos, con descuento u opcionales.

### Contacto

- Datos corporativos ficticios.
- Formulario validado.
- Mensajes de éxito y error.
- Registro de solicitudes en el administrador.

### Footer

Debe identificar el carácter académico del proyecto, el programa Análisis y Desarrollo de Software, el SENA, el año 2026 y la autoría de Juan Esteban Maya · @Yojemr.

## Proceso de venta

1. El visitante consulta una habitación disponible.
2. Selecciona fechas, cantidad de huéspedes y servicios opcionales.
3. El sistema valida los datos y calcula un valor estimado.
4. El visitante envía la solicitud.
5. La solicitud queda registrada como pendiente.
6. El administrador puede cambiarla a confirmada, rechazada o cancelada.

El alcance no incluye pagos reales. La disponibilidad inicial se controla por el estado de la habitación. La detección de cruces entre reservas confirmadas queda prevista como mejora si el cronograma lo permite.

## Contenido de personas reconocidas

No se publicarán testimonios falsos ni se implicará que una persona real visitó el hotel. Se podrán utilizar citas reales y verificadas sobre viajes u hospitalidad, acompañadas de imágenes con licencia compatible o de dominio público y su atribución cuando corresponda.

## Aplicaciones Django

- `hotel_core`: Home, carrusel, información corporativa y citas.
- `hotel_rooms`: habitaciones, imágenes y beneficios.
- `hotel_services`: catálogo de servicios.
- `hotel_reservations`: solicitudes de reserva y servicios seleccionados.
- `hotel_contact`: mensajes de contacto.

## Criterios de finalización

- Los módulos requeridos funcionan como un solo aplicativo.
- El administrador puede gestionar todo el contenido dinámico.
- Las habitaciones y servicios muestran imágenes.
- Los estados visuales de las puertas coinciden con los datos guardados.
- Los formularios validan entradas y muestran mensajes claros.
- La interfaz funciona en computador y dispositivo móvil.
- `python manage.py check`, las migraciones y las pruebas relevantes terminan correctamente.
- No se publican credenciales, entornos virtuales ni datos locales de MariaDB.
