from OpenGL.GL import *


def load_shader(shader_name):
    """Loads, compiles and links vertex and fragment OpenGL shaders with this name.

    Args:
        shader_name: Name of the shader to compile.

    Returns:
        program: Compiled OpenGL shader program.
    """
    shader_path = "microsim/opencl/ramp/shaders/"
    vert = glCreateShader(GL_VERTEX_SHADER)
    with open(f"{shader_path}{shader_name}.vert") as f:
        glShaderSource(vert, f.read())
    glCompileShader(vert)

    frag = glCreateShader(GL_FRAGMENT_SHADER)
    with open(f"{shader_path}{shader_name}.frag") as f:
        glShaderSource(frag, f.read())
    glCompileShader(frag)

    program = glCreateProgram()
    glAttachShader(program, vert)
    glAttachShader(program, frag)
    glLinkProgram(program)
    if glGetProgramiv(program, GL_LINK_STATUS) == GL_FALSE:
        print(glGetProgramInfoLog(program))
        raise ValueError("Shader compilation failed")
    glDeleteShader(vert)
    glDeleteShader(frag)

    return program
