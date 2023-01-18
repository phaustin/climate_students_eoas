# Week 2

Pre-class Reading:
Chapters 1 & 2 of Global Physical Climatology

Due:
Pre-class quiz 1

Learning Goals
- Understand how to update your notebooks from github and practice getting latest updates for notebooks 2, 3 and 4.
- Describe the main features of the global climate system: the atmosphere, ocean, cryosphere and land surface
- Describe the key fluxes in the global energy budget, and explain what variables affect surface temperatures, and why
- Explain what parameterizations are for climate models, why they are necessary, and what their limitations are
- Be able to create a simple 0D climate model in python that solves the energy budget equation to find equilibrium surface temperature for different initial conditions

Labs:
- Lab 2 (zero-dim-ebm)
	- optional Lab 2.1 (analytical-efolding)
- Lab 3 (climate-system-models)

## Syncing your notebooks to the current github commit

- Don't change the files within your climate_students_eoas repo - any changes will get overwritten in this process. 
To run the notebooks, first make a copy of the notebook. We suggest making a new 'working' directory with all of these copies, and then
you can make changes to anything within that directory. When you follow the steps below, this will update all of the notebooks within your repo, but
won't change anything in your working directory. 

- As we make changes to the notebooks, we'll push them to the github repository
  at https://github.com/phaustin/climate_students_eoas

- You can see the commit history: https://github.com/phaustin/climate_students_eoas/commits/student_branch

- To bring those commits into your local repository, do the following:

          cd ~/repos/climate_students_eoas
          git status

  You should see the following line:

          nothing to commit, working tree clean

  If not, then you need to move the files you've changed out of this repository into your work folder
  because all changes will be overwritten in the next step. Now fetch the changes

          git fetch

  Then reset to include the changes (note there are two dashes in front of hard)

          git reset --hard origin/student_branch

  You should see the commit message from my last commit -- to print the last three commits

          git log -3


## Important links

* [Course home](https://phaustin.org/climate_2022)

* [github repository](https://github.com/phaustin/climate_students_eoas.git)

## General references

* [Global Physical Climatology, Dennis Hartmann](https://gw2jh3xr2c.search.serialssolutions.com/?sid=sersol&SS_jc=TC0001767901&title=Global%20physical%20climatology)
 

* [Practical Meteorology](https://www.eoas.ubc.ca/books/Practical_Meteorology)

* [Problem Solving with Python](https://phaustin.github.io/Problem-Solving-with-Python/)

* [A Whirlwind Tour of Python](https://jakevdp.github.io/WhirlwindTourOfPython)

* [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)
