# Electrode visualizer

## Sobre el proyecto
Se trata de una aplicación de escritorio con el objetivo de visualizar datos de electro ensefalogramas. Dirigido a un publico poco experimentado (__ready to use__, __user friendly__)

## Indice
- [Tecnologías](#tecnologías)
- [Instalación/empaquetado](#guía-de-instalación)
- [Advertencias](#advertencias)
- [Uso](#uso)

## Tecnologías
- [DearPyGui.](https://github.com/hoffstadt/DearPyGui) Paquete utilizado para crear la interfaz gráfica
- [Pandas.](https://pandas.pydata.org/) Para la lectura de archivos csv y manipulación de datos.
- [Pyinstaller.](https://pypi.org/project/pyinstaller/) (Opcional) si se busca empaquetar la aplicación como un ejecutable
- [Appimage-builder.](https://appimage-builder.readthedocs.io/en/latest/index.html)(Opcional) si se busca crear una appimage !! Importante al descargar appimage-builder utilizar la version de desarrollo 

## Guía de instalación

### Instalación mediante pip
```
pip install electrode-visualizer
python -m electrode_visualizer
```
#### Recomendaciones:
- revisar si es necesario el entorno virtual de python. la mejor forma de instalación suele ser:
  ```
  python -m pip install electrode-visualizer
  python -m electrode_visualizer
  ```

### Empaquetado para Windows/linux
__El script hace referencia a una imagen "icon.ico" que no se encuentra dentro del repositorio, puedes añadirla o modificar el script para excluirla__
#### Descargar mediante git:
```
git clone git@github.com:IgnaciodelaTorreArias/electrode-visualizer.git
git checkout pyinstaller
```
#### Descargar Zip
Opcionalmente puedes descargar el código fuente como un zip desde github.
[Código fuente rama para ](https://github.com/IgnaciodelaTorreArias/electrode-visualizer/tree/pyinstaller)->Code->Download Zip

#### Empaquetado
Una vez te encuentres en la carpeta del código fuente y con un entorno virtual preferiblemente activado.

Ejecuta el script "config-pyinstaller.bat"

### Construir appimage
__En el script se hace referencia a la imagen "icon.png", esta no se incluye dentro del repositorio pero es indispensable para la construcción__

Pasos:
 - Descargar codigo fuente
 - Descargar appimage-builder
  ```
  python -m pip install git+https://github.com/AppImageCrafters/appimage-builder.git
  ```
 - Usar la receta.
  ```
  python -m appimagebuilder --recipe AppImageBuilder.yml
  ```

## Advertencias:

- En windows cuando se empaqueta a un .exe, los shortcuts parecen no funcionar
- Durante la construcción de ejecutables mediante pyinstaller/appimage se hace referencia a imágenes que no se encuentran dentro del repositorio, asegurarse de incluirlas localmente
- Durante la construcción de la appimage depende de que el entorno de ejecución cuente con python 3.10, esto es porque se puede instalar mediante el gestor de paquetes (apt, por ejemplo), se puede modificar para utilizar pipenv, pyenv u otro gestor de versiones de python, aunque esto complicaría mucho la creación y puede que lo haga mas lento, aunque tengo poca experiencia con la creación de appimages.

## Uso

![Vista previa a abrir un archivo](https://github.com/IgnaciodelaTorreArias/electrode-visualizer/assets/91571670/34a727ac-7cb2-485d-8e40-789b6ac0feab)
![Vista despues de abrir el archivo](https://github.com/IgnaciodelaTorreArias/electrode-visualizer/assets/91571670/249d2cde-619e-4319-9238-b92e79e7805e)
- linea verde: inicio del periodo de tiempo a consultar
- linea roja: fin del periodo de tiempo a consultar
- linea amarilla medio del periodo de tiempo, para recorrer el periodo de tiempo
La linea de tiempo afecta a todos los graficos a la vez
![click izquierdo para ver opciones de vista](https://github.com/IgnaciodelaTorreArias/electrode-visualizer/assets/91571670/b23db6eb-ac11-4df0-9748-3abe5b814b17)
click izquierdo para ver opciones de vista

![sistema de etiquetas](https://github.com/IgnaciodelaTorreArias/electrode-visualizer/assets/91571670/91869569-6edd-469d-bf41-7c6912c0bcd8)
![image](https://github.com/IgnaciodelaTorreArias/electrode-visualizer/assets/91571670/3a1e52dc-4f62-426a-b054-0b526102c481)

Sistema para añadir eleminar etiquetas, permite añadir por periodo o no, si se añade como un periodo de tiempo a la etiqueta se le añade automaticamente un prefijo "inicio_" y "fin_", respectivamente, a la etiqueta, si se tiene como que no es una etiqueta en periodo entonces se toma el punto de inicio como punto unico y no se añade el prefijo.
