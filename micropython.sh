if [ ! -f vendor/micropython/ports/unix/micropython ]; then
	make micropython-build-unix
fi

vendor/micropython/ports/unix/micropython $@
