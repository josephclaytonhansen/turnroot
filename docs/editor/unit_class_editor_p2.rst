Using the Unit/Class Editor, Part 2
======================================
.. contents::

Making your first class
------------------------

Basics
###########

.. image:: 003_c.png
   :alt: Screenshot of Turnroot unit/class editor, class tab
   :align: center

It's time to take Test Unit to the next level- let's make a class for them! We're going to be making a **Basic** tier class. You can change how many tiers of classes there are in the game options (:doc:`game_options`), like this: 

.. image:: 004_act.png
   :alt: Screenshot of Turnroot game options, showing class tier selection
   :align: center

Specifically, we're going to make the default class; or in other words, the base class this unit will have before any reclassing or growth has happened. 

The top row: saving and loading
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The class editor breaks nicely into sections. The top row is for saving and opening classes, the middle section is for setting quick options, and the bottom part is for setting more complex details. Let's start with the top. 

.. image:: 004_tr.png
   :alt: Screenshot of Turnroot game options, showing class tier selection
   :align: center

Much like the unit editor, you need to name your class to save it. This time, however, the class file will be saved as the class name. When you enter a **class name** and press Enter, your class will be saved as ``classes/class name.tructf`` in your game folder. Units are much more likely to share a name, hence the extra step of specifying a filename.

If you can't enter a name, click **New Class**. Now it will work. (Sometimes Turnroot will "load" a class that has empty data, preventing you from making a new class.) 

Once you have a class named, you can click **Load Class** and select it from the list to edit it. 

Let's go ahead and give this class a name so it can start auto-saving. We're going to call it "Traveller". It will be a very simple class. Type "Traveller" in "Class name" and press Enter. Your class is now saved.

You can also provide a **class description**, which is in-game flavor text. Let's do that: go ahead and put something like "A basic voyager with no remarkable abilities. Uses swords, hands, and lances." 

Having said that, we need to make this class actually use those weapon types! One of the most important features of a class is determining what weapon types the unit can use with this class. No class, no weapons. We can move on to the middle section for that.

The middle section: weapon types and basic settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: 004_ms.png
   :alt: Screenshot of Turnroot game options, showing class tier selection
   :align: center

Ignore the right half of this section for a second. You can probably figure out just by looking how to set the weapon types this class can use. If not, it's super simple: just click the checkbox for each weapon type the class can use. In this case, that would be Sword, Lance, and Hands. 

If you don't like your weapon type options, take a look at :doc:`weapon_types` to change them. Remember that you need to do that sooner rather than later. 

With that done, let's head on over to the right side. 

Minimum level and class qualifications
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

**Minimum level** determines what level the unit must have before qualifying for this class. Now's a good time for a sidebar about class qualification. There are three options for how a unit can qualify for a class: level-based, criteria-based, or both. This is a universal setting, and you can set it in game options. (If you're not tired of seeing this link yet, it's here again! :doc:`game_options`) 

* **Level-based** means the only requirement to gain a class is unit level. This can be combined with reclassing items very well. For example, in *Fire Emblem Awakening*, you can reclass to an Advanced class at level 10 if you use a Master Seal. This is a level-based qualification.

* **Criteria-based** means the unit must meet requirements in weapon experience and/or stats. Rather than "the unit can get it or not", the unit has a % chance of getting the class based on how many of the requirements they meet. 

  Here's an example: Let's say you have a class that required a C+ in flying, a B in lance, and a C in sword. If your unit 
  had a C in flying, a B in lance, and a D+ in sword, they would have a 88% 
  chance of being to gain this class, regardless of level. To learn more about how this works, see 
  :doc:`class_qualifications`.

* **Both** combines the two- once the unit hits the specified level, they have a % chance of being able to gain the class. This is the system *Fire Emblem: Three Houses* uses.



