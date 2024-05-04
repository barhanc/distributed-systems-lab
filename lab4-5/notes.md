CORBA = Common Object Request Broker Architecture

Technologia (standard) zapewniająca komunikację pomiędzy obiektami pracującymi w heterogenicznych
systemach komputerowych.

CORBA builds on the OMA (Object Management Architecture) Core Object Model and provides:
- syntax and semantics for IDL

CORBA jest standardem dystrybucji obiektów w sieciach, tak aby operacje na tych obiektach mogły być
wykonywane zdalnie. CORBA nie jest powiązany z zadnym konkretnym językiem programowania, a każdy
język z powiązaniem CORBA może być używany do wywoływania i implementowania obiektów CORBA. Obiekty
są opisane w składni o nazwie Interface Definition Language (IDL).

Komponenty CORBA

* Węzeł integracji żądań obiektów (ORB) <- obsługuje komunikację i zestawianie parametrów w taki
sposób, aby obsługa parametrĻw była przezroczysta dla serwera CORBA i client apps

* Serwer CORBA <- tworzy obiekty CORBA. Serwer umieszcza odwołania do obiektów CORBA w name service,
  dzięki czemu klienci mogą uzyskiwać do nich dostęp

* Name service <- przechowuje odwołania do obiektów CORBA

* Węzeł CORBARequest <- działa jako klient CORBA

Aplikacje serwera CORBA tworzą obiekty CORBA i umieszczają odwołania do obiektów w name service tak
aby klienci mogli wysyłać do nich żądania.

At deployment time, the node contacts a naming service to get an object reference.

When message arrives, the node uses the object reference to call an operation in the CORBA server.


### IDL

Language independence is achieved through the use of a specification meta-language that defines the
interfaces that an object--or a piece of legacy code wrappered to look like an object--presents to
the outside world. As in any object-oriented system, a CORBA object can have its own private data
and its own private methods. The specification of the public data and methods is the interface that
the object presents to the outside world.

IDL is the language that CORBA uses to specify its objects. You do not write procedural code in
IDL--its only use is to specify data, methods, and exceptions.

Each CORBA vendor supplies a compiler that translates IDL specifications into a specific language.
Oracle8i JServer uses the idl2java compiler from Inprise. The idl2java compiler translates your IDL
interface specifications into Java classes. See the Oracle8i Java Tools Reference for more
information on this tool.

```
module hello {
  interface Hello {
    wstring helloWorld();
  };
};
```

IDL consists of a module, which contains a group of related object interfaces. The IDL compiler uses
the module name to name a directory where the Java classes are placed after generation. Also, the
module name is used to name the Java package for the resulting classes.

This module defines a single interface: Hello. The Hello interface defines a single operation:
helloWorld, which takes no parameters and returns a wstring (a wide string, which is mapped to a
Java String).

You can nest modules. For example, an IDL file that specifies the following modules maps to the Java
package hierarchy package org.omg.CORBA.

```
module org {
  module omg {
     module CORBA {
       ...
     };
    ...
  };
   ...
};
```

Kompilator IDL generuje dla danego języka
programowania
    – stub
        ● reprezentuje lokalnie obiekt zdalny
    – skeleton
        ● punkt wejścia do systemu rozproszonego
        ● konwertuje napływające dane, wywołuje metody i zwraca ponownie skonwertowane wyniki
        ● Implementacja obiektu zdalnego to zwykle obiekt dziedziczący po szkielecie zawierający
        implementacje metod z interfejsu IDL


---

Servant - implementation object providing the run time semantic of one or more CORBA objects. A
servant is an instance of the object class; that is, a servant is an instance of the method code you
wrote for each operation in the implementation file.

The Server object is the other programming code entity that you create for a CORBA server
application. The Server object implements operations that execute the following tasks:

Performing basic server application initialization operations, which may include registering
factories managed by the server application and allocating resources needed by the server
application. If the server application is transactional, the Server object also implements the code
that opens an XA resource manager. Instantiating the CORBA objects needed to satisfy client
requests. Performing server process shutdown and cleanup procedures when the server application has
finished servicing requests. For example, if the server application is transactional, the Server
object also implements the code that closes the XA resource manager.

A CORBA object is a virtual entity in the sense that it does not exist on its own, but rather is
brought to life when, using the reference to that CORBA object, the client application requests an
operation on that object. The reference to the CORBA object is called an object reference.

An object adapter is the mechanism that connects a request using an object reference with the proper
code to service that request.

Zdalne wywołanie procedury (ang. remote procedure call, RPC) – protokół zdalnego wywoływania
procedur, stworzony przez firmę Sun i dość popularny w systemach z rodziny Unix, obsługiwany w
bibliotekach języka Java. 

Protokoły tego typu (jak RPC, CORBA, DCOM czy XML-RPC) mają na celu ułatwienie komunikacji pomiędzy
komputerami. Na typowy scenariusz użytkowania takiego protokołu składają się:

Serwer (czyli program oferujący usługi, np. drukowania) przez cały czas nasłuchuje na wybranym
porcie, czy ktoś się z nim nie łączy. Klient (czyli program, który potrzebuje jakiejś usługi od
serwera na innym komputerze) nawiązuje z nim łączność poprzez sieć komputerową. Klient wysyła swoje
dane we wcześniej ustalonym przez programistów klienta i serwera formacie. Serwer realizuje usługę i
odsyła potwierdzenie lub kod błędu. Wymienione protokoły same zapewniają cały powyższy mechanizm
działania, ukrywając go przed klientem. Może on nawet „nie wiedzieć”, że łączy się z innym
komputerem – z punktu widzenia programisty zdalne wywołanie procedury serwera wygląda jak wywołanie
dowolnej innej procedury z programu klienta.


wywołanie synchroniczne blokuje ci "kod" do momentu wykonania i wtedy przechodzi do następnej lini,
a wywołanie asynchroniczne wykonuje się w tle podczas gdy główny kod idzie dalej
