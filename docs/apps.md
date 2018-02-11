
*currency*: Contiene la funcionalidad principal de gestión de entidades y consumidoras
*wallet*: Toda la funcionalidad relativa a pagos: monederos, pagos, transacciones...
*offers*: Modelos y lógica relativa a las ofertas de las entidades
*api*: Contenedor de todas las vistas de la API REST


## Extensión de usuario base
Tanto las entidades (`Entity`) como las consumidoras (`Person`) tienen una relacion 1:1 con usuario, con lo que en
teoría todo usuario debería ser de uno de los dos tipos: entidad o consumidora.

En el momento en el que se crea una entidad o una consumidora asociada a un usuario, se procesa una señal que
añade a dicho usuario al grupo correspondiente: `entities` para el caso de una Entidad, `persons` para el caso de
una consumidora.

Además, extendemos la clase del modelo base de usuario de Django añadiéndole un método `get_related_entity()`.
Este método devuelve una tupla `(type, instance)`, donde `type` será el tipo de objeto asociado al usuario (`entity` o
`person`), e `instance` será dicha instancia. En caso de que el usuario no tenga ninguna instancia asociada, devuelve
`('none', None)`.

Para complementar este método, disponemos del método `get_user_by_related()` para obtener el usuario asociado a una
instancia (ya sea entidad o consumidora) simplemente pasándole el UUID de dicha instancia.