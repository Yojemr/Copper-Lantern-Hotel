# Modelo de datos propuesto

## SiteSettings

Configuración única del sitio:

- nombre del hotel;
- descripción corta y completa;
- logotipo;
- dirección, teléfono y correo;
- horarios de entrada y salida;
- redes sociales;
- estado de publicación.

## HeroSlide

- título;
- subtítulo;
- imagen;
- texto y URL del botón;
- orden;
- activo.

## Quote

- texto;
- autor;
- ocupación o descripción del autor;
- fuente verificable;
- imagen con licencia compatible;
- texto de atribución;
- orden;
- activo.

## Room

- número único;
- nombre comercial;
- slug;
- descripción corta y completa;
- imagen principal;
- precio por noche;
- capacidad;
- descripción de camas;
- estancia mínima;
- estado: disponible, no disponible, próximamente o mantenimiento;
- destacada;
- activa;
- fechas de creación y modificación.

## RoomImage

- habitación;
- imagen;
- texto alternativo;
- orden.

## Service

- nombre;
- slug;
- descripción corta y completa;
- imagen;
- precio;
- unidad de cobro: por estancia, noche, persona o servicio;
- duración;
- permite inclusión en habitaciones;
- destacado;
- activo;
- fechas de creación y modificación.

## RoomServiceBenefit

Relación entre una habitación y un servicio:

- habitación;
- servicio;
- tipo: incluido, con descuento u opcional;
- porcentaje de descuento opcional;
- nota visible;
- restricción única por habitación y servicio.

## Reservation

- código único;
- habitación;
- nombre del cliente;
- correo;
- teléfono;
- fecha de entrada;
- fecha de salida;
- número de huéspedes;
- observaciones;
- estado: pendiente, confirmada, rechazada o cancelada;
- precio estimado de habitación;
- precio estimado de servicios;
- precio total estimado;
- fechas de creación y modificación.

Validaciones:

- la salida debe ser posterior a la entrada;
- los huéspedes no pueden superar la capacidad;
- solo puede solicitarse una habitación disponible;
- los importes no pueden ser negativos.

## ReservationService

- reserva;
- servicio;
- cantidad;
- precio unitario guardado al reservar;
- subtotal;
- indicación de que fue incluido sin costo.

## ContactMessage

- nombre;
- correo;
- teléfono opcional;
- asunto;
- mensaje;
- estado: nuevo, leído o respondido;
- fecha de creación.

## Datos iniciales de demostración

| Habitación | Nombre | Estado | Propósito visual |
|---|---|---|---|
| 101 | The Traveler Room | Disponible | Puerta funcional y opción económica |
| 102 | Maple Comfort | Disponible | Habitación doble clásica |
| 103 | Copper Suite | No disponible | Ejemplo de puerta bloqueada |
| 201 | Heritage King | Próximamente | Ejemplo con cintas de construcción |
| 202 | Lantern Suite | Mantenimiento | Ejemplo con señal de mantenimiento |
| 301 | Presidential Oak Suite | Disponible | Suite destacada con servicios incluidos |
