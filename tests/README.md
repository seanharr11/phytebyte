Within each top-level module you will find:

1. unit/
2. functional/

Let's keep all unit and functional tests separate.

*Unittests* should mock all external datasources, dependencies and libraries, &
only ever excecute the code visible in the method you are testing.
These should poke only at public methods of classes, and not explicitly
(implicit is fine) test any private methods.

*Functional* tests can allow external dependencies to be executed, like DB
queries, third-party library methods, and other classes in this project.
These should "slice" functionalities off the application, and test them.
The functionalities may or may not span multiple modules in the project.
