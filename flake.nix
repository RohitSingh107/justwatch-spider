{
  description = "Fetching my user data from justwatch0";

  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-unstable";
    };
  };

  outputs = {
    self,
    nixpkgs,
    ...
  } @ inputs: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    devShells.${system} = {
      default = pkgs.mkShell {
        buildInputs = with pkgs; [
          postgresql
          sleek # sql formatting

          (python312.withPackages
            (ps:
              with ps; [
                black
                scrapy
                ipython
                httpx
                numpy
                psycopg2 # To Remove
                psycopg
                pycountry
                autopep8
                black
                icecream
                aiofiles
              ]))
        ];

        shellHook = ''

          echo "Welcome to nix shell."
          export PGHOST=$PWD/postgres
          export PGDATA=$PGHOST/data
          export PGDATABASE=postgres
          export PGLOG=$PGHOST/postgres.log

          mkdir -p $PGHOST

          if [ ! -d $PGDATA ]; then
            initdb --auth=trust --no-locale --encoding=UTF8
          fi

          if ! pg_ctl status
          then
            pg_ctl start -l $PGLOG -o "--unix_socket_directories='$PGHOST' --listen_addresses=localhost"
          fi
        '';
      };
    };
  };
}
