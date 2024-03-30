
{
  description = "Fetching my user data from justwatch0";

  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-unstable";
    };
  };

  outputs = {self, nixpkgs, ... }@inputs : 

    let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};

    in

  {
    

    devShells.${system} = {

      default = pkgs.mkShell {
        buildInputs = with pkgs; [
          python312Packages.scrapy
          python312Packages.ipython
          python312Packages.httpx
          python312Packages.numpy
          python312Packages.autopep8
          python312Packages.black
        ];

        shellHook = ''

          echo "Welcome to nix shell."

        '';
      };

    };


  };
}
