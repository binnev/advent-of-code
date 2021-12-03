module example.com/hello

go 1.17

// for the purposes of this dependency, we use .. instead of example.com to locate it
replace example.com/greetings => ../greetings

// created by go mod tidy because it detected an import in hello.go
require example.com/greetings v0.0.0-00010101000000-000000000000
