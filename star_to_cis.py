# Relion coordinates to cisTEM
# Written by Dawid Zyla
#
# This easy script allows you to use Relion picked particles with cisTEM.
# Copy particles.star from export job from Relion directory to the same directory where are the images imported by
# cisTEM. You can choose if you want to create a list of files automaticaly or you will provide the files.txt file
#


from os import listdir

#change here!
pixel_size = 1.34

# change here if you want to create the list of micrographs in cisTEM folder
search_files = False


mrc_cis_full = []
counter = 0
xy_name = []



# search for mrc files in the Image directory (you might want to specify the path, otherwise you need script in the image
# folder
if search_files:
    mrc_cis_full = [f for f in listdir() if '.mrc' in f]

# create a list of files converted by cisTEM using 'ls *mrc > files.txt'
if not search_files:
    with open('files.txt') as mrc_files:
        for i in mrc_files:
            if i != '':
                mrc_cis_full.append(i)

# create a list from particle.star file
with open('particles.star') as particles:
    for particle in particles:

        # remove spaces between columns
        line = particle.split(' ')

        # remove empty elements
        line = list(filter(bool, line))

        # remove header lines
        if len(line) > 10:
            # you might want to adjust the range of file name, here [34:-11]
            # also noticed that relion changes the line of file extract, so you might change line[9] to line[6]
            xy_name.append([line[0], line[1], line[9][34:-11]])

# join particles (x,y) with their images names from cisTEM image names
with open('cistem_coordinates.txt', 'w') as file_out:
    for x in xy_name:

        # match the names of the micrographs from extract to citTEM Image folder files
        if any(x[2] in s for s in mrc_cis_full):
            matching = [s for s in mrc_cis_full if x[2] in s]

            # remove the endline sign
            filename = (matching[0].replace('\n', ''))

            # cisTEM uses Angsrom positions, so Relion x,y coordinates in px have to be multiplied by pixel size
            x_ang = float(x[0]) * pixel_size
            y_ang = float(x[1]) * pixel_size

            # Write the coordinates to file
            print(filename, x_ang, y_ang, file=file_out)
            counter += 1

print('Found ' + str(counter) + ' number of particles and written to cistem_coordinates.txt')
input('Finished! Press enter to exit')
