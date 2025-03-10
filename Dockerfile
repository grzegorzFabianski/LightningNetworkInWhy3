FROM ocaml/opam:ubuntu-24.04-ocaml-4.13 AS build
USER root
ENV PATH=/home/opam/.opam/4.13/bin/:$PATH

COPY <<EOF /bin/control.sh
#!/bin/sh
set -e
echo "Checking that *.mlw files in directory and proof tree match..."
python3 src/checkAllFilesHaveProof.py
echo
echo "Verifying the Statement-Proof separation convention..."
python3 src/checkStatementProofConv.py
echo
echo "Testing simple payment..."
./test.sh
echo
echo "Replaying proofs..."
why3 --extra-config=extraConf.conf -L src replay src
EOF

RUN chown opam /bin/control.sh
RUN chmod +x /bin/control.sh

COPY docker/cvc4-1.8-x86_64-linux-opt /usr/local/bin/cvc4
RUN chown opam /usr/local/bin/cvc4
RUN chmod +x /usr/local/bin/cvc4

RUN apt-get install autoconf libgmp-dev pkg-config zlib1g-dev python3 -y

COPY test.sh /home/opam/
RUN chmod +x test.sh

USER opam
WORKDIR /home/opam/

RUN opam update
RUN opam install why3.1.7.2 alt-ergo.2.4.3 ocamlbuild.0.15.0
RUN why3 config detect

COPY src/* src/
COPY extraConf.conf .

FROM build AS final
COPY --from=build /bin/control.sh /home/opam
ENTRYPOINT [ "/home/opam/control.sh" ]
