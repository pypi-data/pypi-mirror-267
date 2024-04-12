# LILAVATI LIBRARY

The Lilavati library is a Python implementation inspired by the classic mathematical treatise "Leelavati" written by 
the Indian mathematician Bhaskaracharya. This library aims to provide functions and utilities for various mathematical 
computations, drawing inspiration from the methods described in the original work.

## Contributing
   The Lilavati library is a collaborative effort by a group of 6 students:
   
    - Kshitij Joshi
    - Kanishk Mittal
    - Aditya Gopal
    - Surya Narayanan Ghosh
    - Vidya Kaarthika Akella
    - Sejal Satheesh

## Installation
   To install the library, you can use the following command:
   ```bash
   pip install lilavati
   ```
   This will install the library and all its dependencies.
   Then, you can import the library in your Python code using the following command:
   ```python
      import lilavati
   ```
   It has two submodules:
   - Algebra
   - Geometry
   which you can import using the following commands:
   ```python
      from lilavati import Algebra
      from lilavati import Geometry
   ```
   or you can import all the funciton directly as follows 
   ```python
      from lilavati import *
   ```
   then we can use any funciton as follows
   ```python
      lilavati.Algebra.sum_of_permutation([1,2,3,4,5])
   ```

   ## Contribution Guidelines
We welcome contributions to the Lilavati library! If you would like to contribute, please follow these guidelines:

   1. Fork the repository and create a new branch for your contribution.
   2. Make your changes or additions to the codebase.
      1. Ensure that the code follow pylint rules and specify the type usign typing
      2. Wrtie brief description for the funtion in the docstring format
      3. Add your detailes documenation in the respective md file in the folder
      4. for documentation follow the standard template given in [template.md](https://github.com/Project-Leelavati/Leelavati/blob/main/Template.md) file.
   3. Commit your changes and push them to your forked repository.
   4. Submit a pull request to the main repository, explaining the purpose and details of your contribution.
   Our team will review your pull request and provide feedback. Once your contribution is accepted, it will be merged into the main codebase.
   Thank you for your interest in contributing to the Lilavati library!


## Documentation
   For detailed documentation on all available functions and their usage, please refer to following
   - [Algebra.md](https://github.com/Kanishk-mittal/Project-Leelavati/blob/main/lilavati/Algebra/Algebra.md) -> for algebric functions.
   - [Geometry.md](https://github.com/Kanishk-mittal/Project-Leelavati/blob/main/lilavati/Geometry/Geometry.md) -> for geometric functions.
