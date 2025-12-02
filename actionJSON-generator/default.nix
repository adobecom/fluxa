let
  pkgs = import <nixpkgs> {};
in
  pkgs.mkShell {
    name = "actionJSON-generator";
    buildInputs = [
      pkgs.python310
    ];
    shellHook = ''
      if [ -d venv ]; then
        source venv/bin/activate
        echo "Fluxa venv detected. Activate and ready."
      else
        echo "Fluxa venv missing. Run ./setup.sh once before using nix-shell." >&2
      fi
    '';
  }
