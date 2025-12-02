let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
      (pkgs.python312.withPackages (python-pkgs: with python-pkgs; [
        # select Python packages here
        requests
        python-dotenv
        dropbox
        boto3
      ]))
    ];
}
