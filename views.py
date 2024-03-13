import docker
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def execute_code(request):
    try:
        # Extract user input, code, and selected language from the POST request
        input = request.data.get('input')
        user_code = request.data.get('code')
        selected_language = request.data.get('language')

        # Create a directory to store code and input files
        temp_dir = os.getcwd()

# Define file paths for code, input, and output
        code_file_path = os.path.join(temp_dir, 'user_code.py') if selected_language == 'python' else os.path.join(temp_dir, 'user_code.cpp')
        input_file_path = os.path.join(temp_dir, 'input.txt')
        output_file_path = os.path.join(temp_dir, 'output.txt')

        # Write user code and input to files
        
        with open(code_file_path, 'w') as code_file:
            code_file.write(user_code)
        with open(input_file_path, 'w') as input_file:
            input_file.write(input)
        # Create a Docker client
        client = docker.from_env()
# Define the Docker command to execute based on the selected language
        image = "cpp_python"
        command = ""
        if selected_language == 'python':
            command = f'user_code.py python input.txt output.txt'
        elif selected_language == 'cpp':
            command = f'user_code.cpp cpp input.txt output.txt'
        else:
            return Response({'error': 'Unsupported language'}, status=status.HTTP_400_BAD_REQUEST)

        # Run the Docker container
        try:
            container = client.containers.run(
                image,
                command=command,
                volumes={temp_dir: {'bind': '/app', 'mode': 'rw'}},
                remove=True,  # Remove the container when done
                detach=True,  # Run the container in the background
            )

            # Wait for the container to finish execution
            container.wait()

            # Read the output data from the container
            output_data = ""
            with open(output_file_path, 'r') as output_file:
                output_data = output_file.read()

            return Response({'output': output_data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
