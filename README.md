`cq_utils` is a collection of utility functions designed to make it easier to
design parts & assemblies in `cadquery`.

# Dependencies

This project is intended to complement `cadquery`, which is distributed through
`conda`; as such, installing this package (with `pip`) will not install `cadquery`,
and it is assumed you have already installed it yourself.

# Contents

Utilities are grouped into the following modules:
* [`units`](cq_utils/units.py), which is built to make it easier to use `pint` & its unit-wrapped
  quantities in modelling
* [`cadquery`](cq_utils/cadquery.py), which contains utilities which directly interact with `cadquery`
  objects
