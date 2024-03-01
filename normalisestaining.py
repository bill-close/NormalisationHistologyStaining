import argparse
import numpy as np
from PIL import Image

def normalise_staining(img, save_file=None, Io=240, alpha=1, beta=0.15):
    """
    Normalise staining appearance of H&E stained images

    Args:
        img: RGB input image
        save_file: The file to save the normalized image to
        Io: Transmitted light intensity (optional)
        alpha: Parameter for computing minPhi (optional)
        beta: Threshold for transparent pixels (optional)

    Returns:
        Inorm: Normalised image
        H: Hematoxylin image
        E: Eosin image

    Reference: 
        A method for normalising histology slides for quantitative analysis. M.
        Macenko et al., ISBI 2009
    """
    # Reference values for hematoxylin and eosin
    HERef = np.array([[0.5626, 0.2159],
                      [0.7201, 0.8012],
                      [0.4062, 0.5581]])
    maxCRef = np.array([1.9705, 1.0308])

    # Get image dimensions
    h, w, c = img.shape

    # Reshape image to 2D array
    img = img.reshape((-1,3))

    # Calculate optical density
    OD = -np.log((img.astype(float)+1)/Io)

    # Remove pixels with optical density less than beta
    ODhat = OD[~np.any(OD<beta, axis=1)]

    # Compute eigenvectors of covariance matrix of ODhat
    _, eigvecs = np.linalg.eigh(np.cov(ODhat.T))

    # Project ODhat onto plane spanned by eigenvectors corresponding to two largest eigenvalues
    That = ODhat.dot(eigvecs[:,1:3])

    # Compute angle of each point wrt first principal direction
    phi = np.arctan2(That[:,1],That[:,0])

    # Find min and max angles
    minPhi = np.percentile(phi, alpha)
    maxPhi = np.percentile(phi, 100-alpha)

    # Find corresponding vectors
    vMin = eigvecs[:,1:3].dot(np.array([(np.cos(minPhi), np.sin(minPhi))]).T)
    vMax = eigvecs[:,1:3].dot(np.array([(np.cos(maxPhi), np.sin(maxPhi))]).T)

    # Ensure hematoxylin vector is first
    if vMin[0] > vMax[0]:
        HE = np.array((vMin[:,0], vMax[:,0])).T
    else:
        HE = np.array((vMax[:,0], vMin[:,0])).T

    # Reshape OD to 2D array
    Y = np.reshape(OD, (-1, 3)).T

    # Solve linear system to find concentrations
    C = np.linalg.lstsq(HE,Y, rcond=None)[0]

    # Normalise stain concentrations
    maxC = np.array([np.percentile(C[0,:], 99), np.percentile(C[1,:],99)])
    tmp = np.divide(maxC,maxCRef)
    C2 = np.divide(C,tmp[:, np.newaxis])

    # Recreate the image using reference mixing matrix
    Inorm = np.multiply(Io, np.exp(-HERef.dot(C2)))
    Inorm[Inorm>255] = 254
    Inorm = np.reshape(Inorm.T, (h, w, 3)).astype(np.uint8)  

    # Unmix hematoxylin and eosin
    H = np.multiply(Io, np.exp(np.expand_dims(-HERef[:,0], axis=1).dot(np.expand_dims(C2[0,:], axis=0))))
    H[H>255] = 254
    H = np.reshape(H.T, (h, w, 3)).astype(np.uint8)

    E = np.multiply(Io, np.exp(np.expand_dims(-HERef[:,1], axis=1).dot(np.expand_dims(C2[1,:], axis=0))))
    E[E>255] = 254
    E = np.reshape(E.T, (h, w, 3)).astype(np.uint8)

    # Save images if save_file is provided
    if save_file is not None:
        Image.fromarray(Inorm).save(save_file+'.png')
        Image.fromarray(H).save(save_file+'_H.png')
        Image.fromarray(E).save(save_file+'_E.png')

    return Inorm, H, E

if __name__=='__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--imageFile', type=str, default='example1.tif', help='RGB image file')
    parser.add_argument('--saveFile', type=str, default='output', help='Output file name')
    parser.add_argument('--Io', type=int, default=240, help='Transmitted light intensity')
    parser.add_argument('--alpha', type=float, default=1, help='Parameter for computing minPhi')
    parser.add_argument('--beta', type=float, default=0.15, help='Threshold for transparent pixels')
    args = parser.parse_args()

    # Load image
    img = np.array(Image.open(args.imageFile))

    # Normalise staining
    normalise_staining(img=img,
                       save_file=args.saveFile,
                       Io=args.Io,
                       alpha=args.alpha,
                       beta=args.beta)