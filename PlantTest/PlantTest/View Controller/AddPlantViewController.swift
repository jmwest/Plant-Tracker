//
//  AddPlantViewController.swift
//  PlantTest
//
//  Created by John West on 11/5/20.
//  Copyright © 2020 John West. All rights reserved.
//

import UIKit

class AddPlantViewController: UIViewController {

	var delegate: isAbleToReceiveData?
	
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
	
	@IBOutlet weak var plantNameLabel: UILabel!
	@IBOutlet weak var addButton: UIBarButtonItem!
	
	@IBAction func addButtonAction(_ sender: Any) {
		var addPlantDict = [String:String]()
		if let name = plantNameTextFieldOutlet.text {
			addPlantDict["Name"] = name
		}
		if let species = plantSpeciesTextFieldOutlet.text {
			addPlantDict["Species"] = species
		}
		if let water = plantWateringTextFieldOutlet.text {
			addPlantDict["WaterInterval"] = water
		}

		delegate?.pass(data: addPlantDict)
		
		dismiss(animated: true, completion: nil)
	}
	
	@IBAction func plantNameTextFieldDoneEditing(_ sender: UITextField) {
	}
	@IBOutlet weak var plantNameTextFieldOutlet: UITextField!
	
	@IBOutlet weak var plantSpeciesLabel: UILabel!
	
	@IBAction func plantSpeciesTextFieldDoneEditing(_ sender: UITextField) {
	}
	@IBOutlet weak var plantSpeciesTextFieldOutlet: UITextField!
	
	@IBOutlet weak var expectedWateringLabel: UILabel!
	
	@IBAction func plantWateringTextFieldDoneEditing(_ sender: UITextField) {
	}
	@IBOutlet weak var plantWateringTextFieldOutlet: UITextField!
	
	@IBAction func swipeDownGesture(_ sender: UISwipeGestureRecognizer) {
		dismiss(animated: true, completion: nil)
	}
	
	override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
		
		
		guard let uiBarButtonSender = sender as? UIBarButtonItem else {
			return
		}
		
		if addButton == uiBarButtonSender {
			var addPlantDict = [String:String]()
			if let name = plantNameTextFieldOutlet.text {
				addPlantDict["Name"] = name
			}
			if let species = plantSpeciesTextFieldOutlet.text {
				addPlantDict["Species"] = species
			}
			if let water = plantWateringTextFieldOutlet.text {
				addPlantDict["WaterInterval"] = water
			}

			delegate?.pass(data: addPlantDict)
		}
//		dismiss(animated: true, completion: nil)
	}
	
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
