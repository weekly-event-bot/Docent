let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.05";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.mkShellNoCC {
  packages = with pkgs; [
    cowsay
    lolcat
    pkgs.python312
    pkgs.direnv
  ];
  shellHook = ''
              python -m venv .venv
              source .venv/bin/activate
              pip install -r requirements.txt
            '';
}