# Nautas Mascot

[ENGLISH](README.md) | **ESPAÑOL**

Mantenido por Criptonautas. Sin afiliación ni aval de Discourse (Civilized Discourse Construction Kit, Inc.).

Componente de tema para Discourse que pone a **anonist**, la mascota de la comunidad, en el buscador. Invita a preguntar más que a tipear palabras sueltas.

| En reposo | Buscador con foco |
|---|---|
| ![anonist en el buscador](docs/screenshots/mascot-search.png) | ![anonist mirando el buscador](docs/screenshots/mascot-search-focus.png) |

## Qué hace

anonist ocupa el lugar de la lupa y se mueve en pasos, estilo 8 bits:

| Cuándo | Cuadro |
|---|---|
| No pasa nada | respira (sube un píxel) y pestañea cada tanto |
| El buscador recibe foco | mira lo que escribes |
| Haces una pausa al escribir | asiente un píxel |
| La búsqueda está corriendo | piensa, con tres puntos que se encienden |
| Llegan los resultados | guiña |

Con *reducir movimiento* activado en el sistema, queda quieta y solo cambia de cuadro con cada estado.

## Ajustes

| Ajuste | Por defecto | Qué hace |
|---|---|---|
| `search_locations` | `header`, `welcome-banner` | Buscadores donde aparece la mascota |
| `mascot_size` | `32` | Tamaño en píxeles; 32 es el tamaño del dibujo |

## Instalación

**Admin → Apariencia → Temas → Instalar → Desde un repositorio git**, con la URL de este repo. Después se agrega como componente del tema principal. [Cómo instalar un componente de tema](https://meta.discourse.org/t/how-do-i-install-a-theme-or-theme-component/63682)

## Licencia

Código: [MIT](LICENSE). El dibujo de anonist (los cuadros y `docs/`): [CC BY-NC-SA 4.0](CC-BY-NC-SA-4.0.txt), como el resto de los materiales de marca de Criptonautas.
