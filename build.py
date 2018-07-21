import os, shutil

'''
Quick and dirty build script for all the python modules
'''

def setup(dist_dir):
    '''
    Clean up dist directory if exists (delete and recreate)
    :return: dist_dir
    '''
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    return dist_dir


def build_dist(source_folder, destination_folder):
    '''
    Copies all the allowed file types honoring exclusions while preserving folder structure.
    :param source_folder:
    :param destination_folder:
    :return:
    '''
    allowed_file_types = ['.json', '.py', '.html' ,'.yml']
    excludes = ['build.py', 'dist', 'test', 'test_data', '.idea', 'out', '.sh', 'scripts', 'rpmbuild', 'docs']
    # Damn Windows (os.pathsep will not work well with string replace operations)
    if os.name != 'nt':
        path_sep = '/'
    else:
        path_sep = '\\'

    for root, dirs, files in os.walk(source_folder):
        # ensure base dir is not excluded
        if not [e for e in excludes if e in root.split(path_sep)]:
            for item in files:
                src_path = os.path.join(root, item)
                if [a for a in allowed_file_types if src_path.endswith(a)]:
                    if not [e for e in excludes if src_path.endswith(e)]:
                        dst_path = os.path.join(destination_folder, src_path.replace(source_folder + path_sep, ''))
                        shutil.copy2(src_path, dst_path)
            for item in dirs:
                src_path = os.path.join(root, item)
                if not [e for e in excludes if src_path.endswith(e)]:
                    dst_path = os.path.join(destination_folder, src_path.replace(source_folder + path_sep, ''))
                    if not os.path.exists(dst_path):
                        os.mkdir(dst_path)

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.realpath(__file__))
    dist_dir = dist_dir = os.path.join(current_dir, 'dist', os.path.basename(current_dir))
    setup(dist_dir)
    build_dist(current_dir, dist_dir)
    print('Build Complete.Located in: ', dist_dir)
