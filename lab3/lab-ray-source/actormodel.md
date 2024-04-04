# Actor Model

Actor model is a mathematical model of (concurrent) computation based on the consept of **actors**.
Actor is a fundamental unit of computation which embodies three things:

1. Computation (information processing)
2. State (storage)
3. Communication

In the actor model *everything is an actor*. Actors interact with each other by sending a message
(messenger), which is also an actor. Actor can only send a messeage thus an immutable entity.

events are the discrete steps in the ongoing history of an actor's computation.

Each actor has a identifier called an address (it may be a direct physical address such as MAC or
simply a PID). Address is **not** a unique identifier of an actor. Actors can have many addresses
and one address can belong to many actors. All we can do is to send a message to a given address.

### Axioms of Locality

In response to a message an actor can only:
* spawn a finite number of new actors
* send messages to addresses **only** in the message it has just received or in its local state
* update its local state for the next message

The local state (storage) of an actor can include addresses only that:
* where provided when it was created
* that have been received in messages
* that are for actors created by our actor

An actor can send a message to themselves (recursion).

Messages between actors are always sent asynchronuosly.

No requirement on order of message arrival.

# Ray

The FAST compute model
Futures: refernces to objects
Actors : remote class instances
Shared : in-memory distributed object strore
Tasks  : remote functions

Ray core = Tasks + Actors + Objects





