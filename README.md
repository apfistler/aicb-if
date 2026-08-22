# ChatGPT Interface

A bidirectional context-transfer interface for moving information between computing environments and conversational endpoints.

The project provides both **transmit** and **receive** functionality within a single codebase. The initial implementation uses SSH/SCP for transport and Selenium-controlled Chromium for interaction with ChatGPT.

## Project Structure

chatgpt-interface/
├── bin/
│   └── chatgpt
├── etc/
│   └── chatgpt.yaml
├── lib/
│   ├── __init__.py
│   ├── config.py
│   ├── context.py
│   ├── transport.py
│   ├── transmit.py
│   └── receive.py
├── context/
├── tests/
├── README.md
├── LICENSE
└── .gitignore

## Architecture

The project separates context, configuration, transport, and endpoint behavior.

                    chatgpt-interface
                           │
             ┌─────────────┴─────────────┐
             │                           │
         TRANSMIT                     RECEIVE
             │                           │
       Source system                Destination system
             │                           │
             └────── transport ──────────┘
                                         │
                                   Endpoint adapter
                                         │
                                   ChatGPT / Browser

### Transmit

The transmit side is responsible for:

* Accepting context from standard input or files.
* Identifying the destination conversation.
* Loading configuration.
* Preparing context for transport.
* Transferring context to the receiving endpoint.

Example:

cat parser.py | chatgpt cinnamon

If no conversation is specified, the configured default destination is used:

cat parser.py | chatgpt

### Receive

The receive side is responsible for:

* Accepting transferred context.
* Resolving the destination conversation.
* Interacting with the configured endpoint.
* Delivering the context to the destination.

The initial endpoint implementation uses Selenium and Chromium to interact with ChatGPT.

## Configuration

Configuration is stored in:

etc/chatgpt.yaml

Conversation names provide human-readable aliases for conversation identifiers.

Example:

default: current

conversations:

  current:
    id: 6a84f807-c9fc-83ea-99b6-659673465b7c

  cinnamon:
    id: abcdef12-3456-7890-abcd-ef1234567890

  noem:
    id: 12345678-90ab-cdef-1234-567890abcdef

The same configuration model is available to both transmit and receive components.

## Command-Line Interface

The primary interface is:

chatgpt [conversation]

Context is supplied through standard input.

Examples:

echo "Hello" | chatgpt

echo "Hello" | chatgpt cinnamon

cat parser.py | chatgpt cinnamon

grep -n "practice_areas" home.yaml | chatgpt

## Context

Context is treated as a transferable object rather than being tightly coupled to the source command that generated it.

The `context/` directory is used for staged or temporary context during development and transport.

Future implementations may support additional context formats and metadata.

## Transport

The initial transport mechanism is SSH/SCP.

The transport layer is intentionally separated from the transmit and receive logic so that other transport mechanisms can be added later.

Potential future transports include:

* SSH/SCP
* HTTP
* WebSockets
* Local sockets
* Message queues
* API endpoints
* Other machine-to-machine communication mechanisms

## Endpoint Adapters

An endpoint adapter is responsible for delivering context to a particular destination.

The initial endpoint is ChatGPT through a Selenium-controlled Chromium browser.

Future endpoints may include:

* Other conversational AI systems
* Local language models
* Terminal interfaces
* Files
* APIs
* Other applications
* Other computing environments

## Design Principles

### Separation of Concerns

The project separates:

* Context
* Configuration
* Command-line interface
* Transmission
* Transport
* Reception
* Endpoint adapters

Changes to one layer should not require unnecessary changes to the others.

### Human-Readable Destinations

Users should not need to remember implementation-specific identifiers.

Instead of:

chatgpt 6a84f807-c9fc-83ea-99b6-659673465b7c

the preferred interface is:

chatgpt cinnamon

The configuration layer resolves the human-readable name to the underlying destination identifier.

### Transport Independence

The system should not depend on SSH/SCP as a fundamental architectural requirement.

SSH/SCP is the initial transport implementation, not the definition of the interface.

### Endpoint Independence

The interface should not assume that ChatGPT is the only possible destination.

ChatGPT is the initial endpoint implementation.

## Development

The project is intended to run on multiple systems using the same source tree.

For example:

System A
└── chatgpt-interface
    └── transmit

System B
└── chatgpt-interface
    └── receive

Both systems use the same project while performing different roles.

## Current Prototype

The current prototype demonstrates:

1. A command running on a VPS generates context.
2. Context is passed through standard input.
3. The transmit side stages the context.
4. SSH/SCP transfers the context through a reverse SSH connection.
5. The receiving system accepts the context.
6. Selenium controls Chromium.
7. Chromium accesses ChatGPT.
8. The context is inserted into the ChatGPT conversation.

## Future Development

Potential areas for development include:

* Bidirectional communication.
* Persistent endpoint connections.
* Conversation management.
* Context metadata.
* Context history.
* Multiple endpoint types.
* Multiple transport mechanisms.
* Authentication management.
* Error handling and retries.
* Message status and delivery confirmation.
* Context serialization.
* Structured context formats.
* Remote command execution.
* Event-driven communication.

## Status

This project is an experimental prototype.

The architecture, configuration format, command-line interface, and implementation details are subject to change as development continues.

