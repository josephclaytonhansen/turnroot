Class Qualifications
=====================
How can a unit qualify for a class?
-------------------------------------

There are three options for how a unit can qualify for a class: level-based, criteria-based, or both. This is a universal setting, and you can set it in game options.

Level-based means the only requirement to gain a class is unit level. This can be combined with reclassing items very well. For example, in Fire Emblem Awakening, you can reclass to an Advanced class at level 10 if you use a Master Seal. This is a level-based qualification.

Criteria-based means the unit must meet requirements in weapon experience and/or stats. Rather than "the unit can get it or not", the unit has a % chance of getting the class based on how many of the requirements they meet.

Both combines the two- once the unit hits the specified level, they have a % chance of being able to gain the class. This is the system Fire Emblem: Three Houses uses.

Class qualifications: how to set them up
---------------------------------------------

Level-based
^^^^^^^^^^^
This is the simplest by far; all you need to do is set a Minimum Level for the class. If you're using seals or other items to allow levelling up, you can also set that item type from the Class Editor. 

Criteria-based and Both 
^^^^^^^^^^^^^^^^^^^^^^^^
Criteria-based, by itself, is a bit of an odd duck. It's primarily meant to be used as part of Both- however, to shorten things, I'll be talking about (lower-case) both here. 

To set the criteria necessary for a class, click the Class Criteria button in the Class tab of the Unit/Class Editor. This will allow you to set a skill level for each of the skill types. But how does this really work? 

Honestly, it's easier to show than to explain. This spreadsheet will allow you to set the criteria for a class and then test what different skill levels will give you percentage-wise. The first section sets what the class needs. If you need an D in sword, for example, you would need to check E, E+, and D. You need to check everything to the left of the need level. This also applies to the second section, for unit testing: you need to check everything to the left of what the unit has. 

Go ahead and play around with this spreadsheet: you can only check or uncheck checkboxes, nothing else can be edited. 

.. raw:: html

    <iframe width = "700" height = "700" src="https://docs.google.com/spreadsheets/d/1ev_DIvSOgZz5jcThcGsDVVWPjpN4Z7UeiaJNQp_fZmc/edit?usp=sharing&amp;widget=true&amp;headers=false&amp;rm=minimal&amp;chrome=false"></iframe>
    
`Class qualifications interactive spreadsheet <https://docs.google.com/spreadsheets/d/1ev_DIvSOgZz5jcThcGsDVVWPjpN4Z7UeiaJNQp_fZmc/edit?usp=sharing>`_.

The spreadsheet (and the next section) doesn't account for if you turn off "+" skill levels. (This is a rarer use case.) The formula still works without "+"s, exactly the same, no fear.

How does the formula actually work, though?
#############################################

If bowing down to the mighty spreadsheet and trusting it blindly isn't doing it for you, I totally get that. Here's the formula breakdown: be warned, it's a bit technical.

For each skill type (S), let the needed skill level be given a number equal to the number of skill levels leading to the needed level. Let this number be Sn. (For example, a D would have an Sn of 3: E, E+, D = 3.) 

Let the acquired skill level be Sa. This number is calculated the same, unless Sa > Sn, in which case Sa = Sn. (If a unit is overqualified, it doesn't boost their chances.)

Let ``Sd = abs(Sa - Sn)``. 

Let ``Sp = Sa - 1.5 x Sd``.

For each S, let A...Z be S. Let N be the total number of S. (The first S would be A, the next B.) Let ``P = {Ap + Bp...+Np}``.

Let C be the final percentage. ``C = P - (.05 x (100 - P))``.
