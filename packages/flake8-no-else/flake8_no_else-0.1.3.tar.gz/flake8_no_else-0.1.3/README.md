- [flake8-no-else](#flake8-no-else)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Rules Enforced](#rules-enforced)
  - [Configuration](#configuration)
  - [Motivation](#motivation)
  - [Contributing](#contributing)
  - [License](#license)


# flake8-no-else

`flake8-no-else` is a plugin for Flake8 that promotes cleaner and more maintainable code by enforcing the Object Calisthenics rule: "Do Not Use ELSE." This plugin discourages the use of `else`, `elif`, and ternary operators in Python code, encouraging developers to use guard clauses and other techniques to keep code flat and prevent deep nesting.

## Installation

You can install `flake8-no-else` using pip:

```bash
pip install flake8-no-else
```

## Usage

Once installed, `flake8-no-else` will automatically integrate with Flake8. Run Flake8 as you normally would:

```bash
flake8 your_project_directory
```

`flake8-no-else` will check for the presence of `else`, `elif`, and ternary expressions and flag them as violations.

## Rules Enforced

- **NOE100**: Use of `else`
- **NOE101**: Use of `elif`
- **NOE102**: Use of ternary operator (`condition ? true_value : false_value`)

## Configuration

There are no specific configurations required for `flake8-no-else`. It works out-of-the-box once installed. However, you can exclude specific files or directories through your standard `.flake8` configuration file.

Example `.flake8` configuration:

```ini
[flake8]
exclude = tests/*
max-line-length = 120
```

## Motivation

The motivation behind this plugin is to encourage developers to follow the "Do Not Use ELSE" rule of Object Calisthenics. This rule aims to reduce the complexity of code by avoiding multiple conditional branches, which often lead to deeply nested structures and can make code harder to read and maintain.

## Contributing

Contributions to `flake8-no-else` are welcome! If you have suggestions for improvements or have found a bug, please open an issue or submit a pull request.

## License

Distributed under the MIT License. See `LICENSE` file for more information.