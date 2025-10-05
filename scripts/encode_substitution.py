import json
from random import shuffle

from typer import Typer, echo

main = Typer(invoke_without_command=False)


@main.command()
def encode_substitution(
    message: str,
    print_substitution: bool = False,
) -> None:
    characters = [chr(i + ord("A")) for i in range(26)]
    shuffle(characters)

    cipher = "".join(
        characters[ord(c) - ord("A")] if "A" <= c <= "Z" else c for c in message.upper()
    )

    echo(f"Chiffre: {cipher}")

    if print_substitution:
        echo("Substitution:")
        echo(json.dumps(characters))


if __name__ == "__main__":
    main()
