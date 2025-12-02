let
  pkgs = import <nixpkgs> {};
in
  pkgs.mkShell {
    name = "actionJSON-generator";
    buildInputs = [
      pkgs.python310
    ];
    shellHook = ''
      ./setup.sh
      source venv/bin/activate
    '';
  }
