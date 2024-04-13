import h5py
import numpy as np
from PIL import Image
import io
import pandas as pd
import pickle
import json
import os
import uuid
from openslide import OpenSlide, OpenSlideUnsupportedFormatError

class TiffX:
    def __init__(self,
                 filename=None, # Path to the .tiffx file to read the data.
                 construct_from_file=None, # Path to the .tiff or .svs file to store as raw binary data.
                 ):
        self.data = {}
        self.filename = filename
        if filename:
            if os.path.exists(filename):
                self.load(filename)
            else:
                raise FileNotFoundError(f"File {filename} not found")
        elif construct_from_file:
            self.set_tiff(construct_from_file)
            
    def set_tiff(self, filename):
        """Set and store a TIFF file as raw binary data for future use."""
        try:
            with open(filename, 'rb') as file:
                self.data['wsi_image'] = {
                    'type': 'binary',
                    'data': file.read()  # Read the entire file as binary data
                }
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found")
        except Exception as e:
            raise IOError(f"Error reading the .svs file: {str(e)}")


    def __getattr__(self, name):
        if 'slide' in self.__dict__:
            slide = self.__dict__['slide']
            if slide is not None and hasattr(slide, name):
                return getattr(slide, name)
        raise AttributeError(f"'TiffX' object has no attribute '{name}'")
        
    def __str__(self):
        return self._generate_structure()

    def __repr__(self):
        return self._generate_structure()

    def _generate_structure(self):
        lines = ["|-- metadata"]
        types = {'array': [], 'dataframe': [], 'image': []}
        details = {}

        # Check if self.slide is initialized and append information about it
        if self.slide is not None:
            lines.append("|-- slide: OpenSlide object")
        
        # Collect details about each item for display
        for key, value in self.data.items():
            if value['type'] in types:
                types[value['type']].append(key)
                if value['type'] == 'array':
                    # Shape and data type of the numpy array
                    details[key] = f"{value['data'].dtype}, shape={value['data'].shape}"
                elif value['type'] == 'dataframe':
                    # Shape of the dataframe
                    details[key] = f"shape={value['data'].shape}"
                elif value['type'] == 'image':
                    # Check if data is bytes, and convert to an image object for size fetching
                    if isinstance(value['data'], bytes):
                        img = Image.open(io.BytesIO(value['data']))
                        details[key] = f"{img.size}"
                    elif isinstance(value['data'], Image.Image):
                        details[key] = f"{value['data'].size}"
                    else:
                        details[key] = "Unknown format"

        # Build the structure display string
        for category in ['array', 'dataframe', 'image']:
            count = len(types[category])
            lines.append(f"|-- [{count}] {category}")
            for name in sorted(types[category]):
                dimension = details.get(name, 'Unknown')
                lines.append(f"|       |-- \"{name}\" ({dimension})")

        return "\n".join(lines)
    

    def set_metadata(self, metadata):
        self.data['metadata'] = {'type': 'metadata', 'data': json.dumps(metadata)}

    def add_array(self, id, array):
        self.data[id] = {'type': 'array', 'data': array}

    def remove_array(self, id):
        if id in self.data and self.data[id]['type'] == 'array':
            del self.data[id]

    def add_df(self, id, dataframe):
        self.data[id] = {'type': 'dataframe', 'data': dataframe}

    def remove_df(self, id):
        if id in self.data and self.data[id]['type'] == 'dataframe':
            del self.data[id]

    def add_image(self, id, image):
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        self.data[id] = {'type': 'image', 'data': img_buffer.getvalue()}

    def remove_image(self, id):
        if id in self.data and self.data[id]['type'] == 'image':
            del self.data[id]

    def save(self, filename):
        with h5py.File(filename, 'w') as h5file:
            # Save metadata
            if 'metadata' in self.data:
                h5file.create_dataset('metadata', data=json.dumps(self.data['metadata']['data']).encode('utf-8'))

            # Save the wsi_image if present and is in binary format
            if 'wsi_image' in self.data and self.data['wsi_image']['type'] == 'binary':
                # Convert the raw binary data into a numpy array of type uint8
                bin_data = np.frombuffer(self.data['wsi_image']['data'], dtype=np.uint8)
                h5file.create_dataset('wsi_image', data=bin_data)

            # Create groups for different types
            for dtype in ['array', 'dataframe', 'image']:
                group = h5file.create_group(dtype)
                for key, value in self.data.items():
                    if value['type'] == dtype:
                        if dtype == 'array':
                            group.create_dataset(key, data=value['data'])
                        elif dtype == 'dataframe':
                            df_buffer = io.BytesIO()
                            value['data'].to_parquet(df_buffer, index=False)
                            df_buffer.seek(0)
                            group.create_dataset(key, data=np.array(df_buffer.getvalue(), dtype='bytes'))
                        elif dtype == 'image':
                            # Convert bytes back to an image for saving
                            if isinstance(value['data'], bytes):
                                img_buffer = io.BytesIO(value['data'])
                                img = Image.open(img_buffer)
                            else:
                                img = value['data']  # Assuming it's still an image object
                            img_buffer = io.BytesIO()
                            img.save(img_buffer, format='PNG')
                            img_buffer.seek(0)
                            group.create_dataset(key, data=np.array(img_buffer.getvalue(), dtype='bytes'))
    
    def load(self, filename):
        with h5py.File(filename, 'r') as h5file:
            if 'metadata' in h5file:
                self.data['metadata'] = {'type': 'metadata', 'data': json.loads(h5file['metadata'][()].decode('utf-8'))}

            if 'wsi_image' in h5file:
                binary_data = h5file['wsi_image'][()]
                temp_filename = os.path.join("/tmp", f"tiffx_temp_loaded_wsi_{uuid.uuid4()}.tiffxwsi")
                with open(temp_filename, 'wb') as temp_file:
                    temp_file.write(binary_data)

                try:
                    self.slide = OpenSlide(temp_filename)
                    print("WSI file loaded successfully and is ready for use with OpenSlide.")
                except OpenSlideUnsupportedFormatError:
                    os.remove(temp_filename)  # Clean up the temp file if loading fails
                    print("Failed to load the WSI file with OpenSlide.")
                    self.slide = None

            for dtype in ['array', 'dataframe', 'image']:
                group = h5file.get(dtype, {})
                for key, item in group.items():
                    if dtype == 'array':
                        self.data[key] = {'type': 'array', 'data': item[:]}
                    elif dtype == 'dataframe':
                        df_buffer = io.BytesIO(item[()])
                        self.data[key] = {'type': 'dataframe', 'data': pd.read_parquet(df_buffer)}
                    elif dtype == 'image':
                        image_data = io.BytesIO(item[()])
                        self.data[key] = {'type': 'image', 'data': Image.open(image_data)}


    def load_metadata(self):
        return self.data.get('metadata', {}).get('data')

    def load_df(self, id):
        if id not in self.data or self.data[id]['type'] != 'dataframe':
            raise ValueError(f"DataFrame with ID '{id}' not found.")
        return self.data[id]['data']

    def load_array(self, id):
        if id not in self.data or self.data[id]['type'] != 'array':
            raise ValueError(f"Array with ID '{id}' not found.")
        return self.data[id]['data']

    def load_image(self, id):
        if id not in self.data or self.data[id]['type'] != 'image':
            raise ValueError(f"Image with ID '{id}' not found.")
        
        image_data = self.data[id]['data']
        if isinstance(image_data, bytes):
            # Convert bytes back to an image if it's not already an image object
            image_data = io.BytesIO(image_data)
            image = Image.open(image_data)
        elif isinstance(image_data, Image.Image):
            image = image_data
        else:
            raise TypeError("Stored image data is neither bytes nor a recognizable image object.")
        
        return image
    