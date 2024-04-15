# Space Rescue - A Escape Coding Adventure

[![Servier Powered](https://raw.githubusercontent.com/servierhub/.github/main/badges/powered.svg)](https://github.com/ServierHub/)

A pyray game for escape coding adventure.

## Description

This game allows to build an adventure where the player must unlock challenges by coding a solution to a
problem. The system will check the validity of the result (possible result and test coverage) and let the player
navigate in the game.

### Mission

You are the AI of the NCC-DaFa spaceship, the state-of-the-art ship of the Earth fleet. After an accident, the crew is
disabled and must be bring back to a planet to be rescued. Following your directives, you have to plot a safe course to
the planet indicated by the Earth Command. Earth Command sent a message in your logs when they became aware of the
situation.

### Bacis Mission Outlines

* [ ] Find the coordinates of the planets in message using embeddings, llm, etc ...
* [ ] Plot a course from start to a random planet, going through hyperspace tunnels using BFS
* [ ] Avoid asteroid (recursive)
* [ ] Avoid Obstacles (Reinforcement Learning)

## Getting Started

### Dependencies

* Python 3.11 or above
* Poetry 1.7.1 or above

### Python Installation

For more details, see the [Installation Guide](https://www.python.org/)

### Poetry Installation

Install using pip:

```bash
pip install poetry
```

For more details, see the [Installation Guide](https://python-poetry.org/docs/)

### Build and install locally

Install all dependencies with the following command:

```bash
poetry install
```

### Run the game framework

Run the game with the following command:

```bash
poetry run python -m spacerescue
```

### Documentation

Build the documentation with the following command:

```bash
poetry run mkdocs build
```

Please find more details [here](https://romualdrousseau.gitlab.io/spacerescue)

## Contribute

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors

* Romuald Rousseau, romuald.rousseau@servier.com

## Version History

* 0.2.4
* 0.2.3
* 0.2.2
* 0.2.1
* 0.2.0
* 0.1.0
* Initial Release