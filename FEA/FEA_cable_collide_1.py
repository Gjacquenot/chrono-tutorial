# =============================================================================
# PROJECT CHRONO - http:#projectchrono.org
#
# Copyright (c) 2014 projectchrono.org
# All right reserved.
#
# Use of this source code is governed by a BSD-style license that can be found
# in the LICENSE file at the top level of the distribution and at
# http:#projectchrono.org/license-chrono.txt.
#
# =============================================================================
# Author: Simone Benatti
# =============================================================================
#
# Create a falling cable using FEA module (FEA tutorial n.1)
#
# This cable is made with N beam elements of ChElementANCFcable type. They are
# added to a ChMesh and then the first node is connected to the absolute
# reference using a constraint.
#
# The cable falls under the action of gravity alone, acting in the negative
# Y (up) direction.
#
# The simulation is animated with Irrlicht.
#
# =============================================================================

import pychrono as chrono
import pychrono.fea as fea
import pychrono.irrlicht as chronoirr



# 0. Set the path to the Chrono data folder
CHRONO_DATA_DIR = "C:/codes/Chrono/Chrono_Source/data/"
chrono.SetChronoDataPath(CHRONO_DATA_DIR)

# 1. Create the physical system that will handle all finite elements and constraints.

#    Specify the gravitational acceleration vector, consistent with the
#    global reference frame having Y up (ISO system).
system = chrono.ChSystemNSC()
system.Set_G_acc(chrono.ChVectorD(0, -9.81, 0))


# 2. Create the mesh that will contain the finite elements, and add it to the system

mesh = fea.ChMesh()

system.Add(mesh)


# 3. Create a material for the beam finite elements.

#    Note that each FEA element type requires some corresponding
#    type of material. Here we will use ChElementCableANCF elements:
#    they use a material of type ChBeamSectionCable, so let's do

beam_material = fea.ChBeamSectionCable()
beam_material.SetDiameter(0.01)
beam_material.SetYoungModulus(0.01e9)
beam_material.SetBeamRaleyghDamping(0.01)


# 4. Create the nodes

#    - We use a simple for() loop to create nodes along the cable.
#    - Nodes for ChElementCableANCF must be of ChNodeFEAxyzD class
#      i.e. each node has 6 coordinates: position, direction, where
#      direction is the tangent to the cable.
#    - Each node must be added to the mesh, ex.  mesh.Add(my_node)
#    - To make things easier in the following, we store node pointers
#      into an optional 'beam_nodes' array, i.e. a std::vector<>, later we
#      can use such array for easy creation of elements between the nodes.

beam_nodes = []

length = 1.2  # beam length, in meters
N_nodes = 16
for i_ni in range(N_nodes)  :
    # i-th node position
    position = chrono.ChVectorD(length * (i_ni / (N_nodes - 1)),  # node position, x
                                0.5,                                  # node position, y
                                0)                                   # node position, z

    # i-th node direction
    direction = chrono.ChVectorD(1.0, 0, 0)

    # create the node
    node = fea.ChNodeFEAxyzD(position, direction)

    # add it to mesh
    mesh.AddNode(node)

    # add it to the auxiliary beam_nodes
    beam_nodes.append(node)



# 5. Create the elements

#    - We use a simple for() loop to create elements between the
#      nodes that we already created.
#    - Each element must be set with the ChBeamSectionCable material
#      that we already created
#    - Each element must be added to the mesh, ex.  mesh.Add(my_element)

for ie in range(N_nodes - 1) :
    # create the element
    element = fea.ChElementCableANCF()

    # set the connected nodes (pick two consecutive nodes in our beam_nodes container)
    element.SetNodes(beam_nodes[ie], beam_nodes[ie + 1])

    # set the material
    element.SetSection(beam_material)

    # add it to mesh
    mesh.AddElement(element)



# 6. Add constraints

#    - Constraints can be applied to FEA nodes
#    - For the ChNodeFEAxyzD there are specific constraints that
#      can be used to connect them to a ChBody, namely
#      ChLinkPointFrame and ChLinkDirFrame
#    - To attach one end of the beam to the ground, we need a
#      'truss' ChBody that is fixed.
#    - Note. An alternative, only when the node must be fixed 
#      to absolute reference, is not using constraints, and just
#      use: beam_nodes[0].SetFixed(True)  (but would fix also dir)

truss = chrono.ChBody()
truss.SetBodyFixed(True)
system.Add(truss)

# lock an end of the wire to the truss
constraint_pos = fea.ChLinkPointFrame()
constraint_pos.Initialize(beam_nodes[0], truss)
system.Add(constraint_pos)


## -------------------------------------------------------------------------
## EXERCISE 1a
##
## Add a cylinder.
## Suggested size: 0.02 radius, 0.1 height, density:1000.
## Hint: use the ChBodyEasyCylinder to make the cylinder, pass size as 
## parameters in construction.
## 
## -------------------------------------------------------------------------


# TO DO ...


## -------------------------------------------------------------------------
## EXERCISE 1b
##
## Attach the cylinder to the free end of the cable.
## Hint: use the ChLinkPointFrame to connect the cylinder and the end node.
## 
## -------------------------------------------------------------------------

# TO DO ...


# 7. Make the finite elements visible in the 3D view

#   - FEA fisualization can be managed via an easy
#     ChVisualizationFEAmesh helper class.
#     (Alternatively you could bypass this and output .dat
#     files at each step, ex. for VTK or Matalb postprocessing)
#   - This will automatically update a triangle mesh (a ChTriangleMeshShape
#     asset that is internally managed) by setting proper
#     coordinates and vertex colours as in the FEA elements.
#   - Such triangle mesh can be rendered by Irrlicht or POVray or whatever
#     postprocessor that can handle a coloured ChTriangleMeshShape).
#   - Do not forget AddAsset() at the end!

mvisualizebeamA = fea.ChVisualizationFEAmesh(mesh)
mvisualizebeamA.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_ANCF_BEAM_AX)
mvisualizebeamA.SetColorscaleMinMax(-0.005, 0.005)
mvisualizebeamA.SetSmoothFaces(True)
mvisualizebeamA.SetWireframe(False)
mesh.AddAsset(mvisualizebeamA)

mvisualizebeamC = fea.ChVisualizationFEAmesh(mesh)
mvisualizebeamC.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_DOT_POS)  # E_GLYPH_NODE_CSYS for ChNodeFEAxyzrot
mvisualizebeamC.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_NONE)
mvisualizebeamC.SetSymbolsThickness(0.006)
mvisualizebeamC.SetSymbolsScale(0.005)
mvisualizebeamC.SetZbufferHide(False)
mesh.AddAsset(mvisualizebeamC)


# 8. Configure the solver and timestepper

#    - the default SOLVER_SOR of Chrono is not able to manage stiffness matrices
#      as required by FEA! we must switch to a different solver.
#    - We pick the SOLVER_MINRES solver and we configure it.
#    - Note that if you build the MKL module, you could use the more precise MKL solver.

solver = chrono.ChSolverMINRES()
solver.SetMaxIterations(200)
solver.SetTolerance(1e-10)
solver.EnableWarmStart(True)
system.SetSolver(solver)

# Change integrator:
system.SetTimestepperType(chrono.ChTimestepper.Type_EULER_IMPLICIT_LINEARIZED)  # default: fast, 1st order
# system.SetTimestepperType(ChTimestepper::Type::HHT)  # precise, slower, might iterate each step


# 9. Prepare visualization with Irrlicht
#    Note that Irrlicht uses left-handed frames with Y up.

# Create the Irrlicht application and set-up the camera.
application = chronoirr.ChIrrApp(system,                             # pointer to the mechanical system
                                 "FEA cable collide demo",           # title of the Irrlicht window
                                 chronoirr.dimension2du(1024, 768),  # window dimension (width x height)
                                 chronoirr.VerticalDir_Y,            # camera vertical direction
                                 False,                              # use full screen?
                                 True,                               # enable stencil shadows?
                                 True)                               # enable antialiasing?

application.AddLogo()
application.AddSkyBox()
application.AddTypicalLights()
application.AddCamera(chronoirr.vector3df(0.1, 0.2, -2.0),  # camera location
                      chronoirr.vector3df(0.0, 0.0, 0.0))   # "look at" location

# Let the Irrlicht application convert the visualization assets.
application.AssetBindAll()
application.AssetUpdateAll()


# 10. Perform the simulation.

# Specify the step-size.
application.SetTimestep(0.01)
application.SetTryRealtime(True)


while application.GetDevice().run() :
    # Initialize the graphical scene.
    application.BeginScene()

    # Render all visualization objects.
    application.DrawAll()

    # Draw an XZ grid at the global origin to add in visualization.
    chronoirr.drawGrid(application.GetVideoDriver(), 0.1, 0.1, 20, 20,
                       chrono.ChCoordsysD(chrono.ChVectorD(0, 0, 0), chrono.Q_from_AngX(chrono.CH_C_PI_2)),
                       chronoirr.SColor(255, 80, 100, 100), True)

    # Advance simulation by one step.
    application.DoStep()

    # Finalize the graphical scene.
    application.EndScene()




