# TexGen-script for generating RVE
# Written by:
    # Anthon Rindsäter (anthonr@chalmers.se)
    # Fiona Coates (fionac@chalmers.se)
# Date last modified: 2024-12-18

##############################################################################

# Import nessecary packages
from _Embedded import *
from TexGen.Core import *
from TexGen.Renderer import *
from TexGen.Export import *
from TexGen.WeavePattern import *
from TexGen.WiseTex import *
from TexGen.FlowTex import *
import math
import runpy

############################ CT-scan measurements ############################
# 326 voxels in X-dir => 19.805574496 mm in X-dir
# 315 voxels in Y-dir => 19.13728824 mm in Y-dir
# 76 voxels in Z-dir => 4.617250496 mm in Z-dir
############################ CT-scan measurements ############################

# Set number of yarns in the X- and Y-direction:
NumWarpYarns = 8
NumWeftYarns = 8

# Set initial spacing between yarns:
WarpSpacing = 1
WeftSpacing = 1

# Set initial height of yarns:
WarpHeight = 0.4
WeftHeight = 0.4

# Create the textile:
Textile = CTextileOrthogonal(NumWarpYarns, NumWeftYarns, WarpSpacing, WeftSpacing, WarpHeight, WeftHeight, True)

# Set the ratio of X-/Z-yarns (1 to 1 means as many through thickness
# yarns as yarns in the X-direction):
Textile.SetWarpRatio(1)
Textile.SetBinderRatio(1)

# Set number of yarn layers and update the textile:
NumWarpLayers = 5
NumWeftLayers = 6
Textile.SetupLayers(NumWarpLayers, NumWeftLayers)

# Set yarn widths, heights and spacings based on measurements from CT-scan
# -------------------------------------------------------------------------- #
# Yarns in X-direction:
Textile.SetWarpYarnWidths(2.4301)
Textile.SetWarpYarnHeights(0.3645)
Textile.SetWarpYarnSpacings(2.45+0.167)

# Yarns in Z-direction:
Textile.SetBinderYarnWidths(2.0656)
Textile.SetBinderYarnHeights(0.6075)
Textile.SetBinderYarnSpacings(2+0.167)

# Yarns in Y-direction
Textile.SetYYarnWidths(2.0049)
Textile.SetYYarnHeights(0.4253)
Textile.SetYYarnSpacings(2.476)
# -------------------------------------------------------------------------- #

# Set the power of the power ellipses used for the cross section:
Textile.SetWarpYarnPower(0.2)
Textile.SetWeftYarnPower(0.2)
Textile.SetBinderYarnPower(0.5)

# Swap positions of the through thickness yarns, the through thickness yarns
# are created on top of the textile the positions where the through thickness
# yarns should be at the bottom have to be specified. Position here behaves 
# like coordinates, where position 1, 1 for example refers to the 1 yarn in the
# X-direction and 1 yarn in the Y-direction from origo.
# -------------------------------------------------------------------------- #
Textile.SwapBinderPosition(1, 1)
Textile.SwapBinderPosition(3, 1)
Textile.SwapBinderPosition(5, 1)
Textile.SwapBinderPosition(7, 1)

Textile.SwapBinderPosition(0, 3)
Textile.SwapBinderPosition(2, 3)
Textile.SwapBinderPosition(4, 3)
Textile.SwapBinderPosition(6, 3)
Textile.SwapBinderPosition(8, 3)

Textile.SwapBinderPosition(1, 5)
Textile.SwapBinderPosition(3, 5)
Textile.SwapBinderPosition(5, 5)
Textile.SwapBinderPosition(7, 5)

Textile.SwapBinderPosition(0, 7)
Textile.SwapBinderPosition(2, 7)
Textile.SwapBinderPosition(4, 7)
Textile.SwapBinderPosition(6, 7)
Textile.SwapBinderPosition(8, 7)
# -------------------------------------------------------------------------- #

# Create a default domain to fit the textile:
Textile.AssignDefaultDomain()

# Set yarn/fibre properties:
Textile.SetFibreDiameter(WARP, 0.007, "mm")
Textile.SetFibreDiameter(WEFT, 0.007, "mm")
Textile.SetFibreDiameter(BINDER, 0.007, "mm")
Textile.SetFibresPerYarn(WARP, 12000)
Textile.SetFibresPerYarn(WEFT, 12000)
Textile.SetFibresPerYarn(BINDER, 12000)

# Set the target thickness for the refined textile:
Textile.SetThickness(5.3)

# Set the maximum volume fraction allowed in the refining process:
Textile.SetMaxVolFraction(0.78)

# Reset the domain height to suit the refined textile:
Textile.SetDomainZValues()

# Set custom domain to fit dimensions of RVE from CT-scan measurements
Domain = CDomainPlanes(XYZ(0, 0+0.65, -0.6075+0.15), XYZ(19.81, 19.14+0.65, 4.982-0.15))
Textile.AssignDomain(Domain)

# Add the textile:
AddTextile(Textile)