# NVDA Rust Example

This Rust crate contains example code to interface with `nvdaControllerClient`.
The following instructions assume you have Rust installed.

To run the example:

1. Ensure the client library is built with `scons client` from the root of the NVDA repository.
1. Run `cargo test`. While this crate has no tests, it ensures that our example is built.
1. Navigate to the architecture folder within the `controllerClient` folder, e.g. `..\..\x64`.
1. Run `cargo run --example example_rust --manifest-path ..\examples\example_rust\Cargo.toml --release`.
