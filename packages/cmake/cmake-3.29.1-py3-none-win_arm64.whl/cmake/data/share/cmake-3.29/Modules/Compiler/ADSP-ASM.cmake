include(Compiler/ADSP)
__compiler_adsp(ASM)

set(CMAKE_ASM_SOURCE_FILE_EXTENSIONS asm)
set(CMAKE_ASM_OUTPUT_EXTENSION ".o" )
set(CMAKE_ASM_COMPILE_OBJECT "<CMAKE_ASM_COMPILER> <DEFINES> <INCLUDES> <FLAGS> -o <OBJECT> <SOURCE>")
