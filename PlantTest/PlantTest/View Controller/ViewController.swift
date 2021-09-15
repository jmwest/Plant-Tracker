//
//  ViewController.swift
//  PlantTest
//
//  Created by John West on 11/5/20.
//  Copyright © 2020 John West. All rights reserved.
//

import UIKit
import CoreData

class ViewController: UIViewController, isAbleToReceiveData {
	
	// Delegate Protocol Definition
	func pass(data: Dictionary<String, String>) {
		savePlantToCoreData(data: data)
		
		fetchPlants()
	}
	
	// Variable Declaration
	@IBOutlet weak var plantCollectionView: UICollectionView!
	@IBOutlet weak var flowLayout: UICollectionViewFlowLayout!
	@IBOutlet weak var addPlantButton: UIButton!
	
	let context = (UIApplication.shared.delegate as! AppDelegate).persistentContainer.viewContext
	
	var items:[PlantArchitecture]?
	
	// Segue functions
	override func prepare(for segue: UIStoryboardSegue, sender: Any?) {

		if let vcAddPlant = segue.destination as? AddPlantViewController {
			vcAddPlant.delegate = self
		}
		
		//present(vcAddPlant, animated: true, completion: nil)
	}
	
	@objc func myUnwindAction( unwindSegue: UIStoryboardSegue) {
	}

	// viewDidLoad
	override func viewDidLoad() {
		super.viewDidLoad()
		// Do any additional setup after loading the view.
		plantCollectionView.dataSource = self
		plantCollectionView.delegate = self
		//plantCollectionView.delegate = self as? UICollectionViewDelegate
		
		view.bringSubviewToFront(addPlantButton)

		fetchPlants()
	}

	// Core Data Management
	func fetchPlants() {
		
		do {
			self.items = try context.fetch(PlantArchitecture.fetchRequest()) as? [PlantArchitecture]
		}
		catch  {
			print("Failed to fetchPlants")
		}
		
		DispatchQueue.main.async {
			self.plantCollectionView.reloadData()
		}
	}
	
	func savePlantToCoreData(data: Dictionary<String, String>) {
		
		let newPlant = PlantArchitecture(context: self.context)
		
		newPlant.name = data["Name"]
		newPlant.species = data["Species"]
		newPlant.expectedWatering = Int16(data["WateringInterval"] ?? "") ?? 0
		
		// Save context
		do {
			try self.context.save()
		} catch {
			print("Failed to save the new plant.")
		}
		
	}
}

// Delegate Protocol Declaration
protocol isAbleToReceiveData {
	func pass(data: Dictionary<String, String>)
}

// UICollectionViewDataSource Extension Definition
extension ViewController: UICollectionViewDataSource {
	func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
		let context = (UIApplication.shared.delegate as! AppDelegate).persistentContainer.viewContext
		
		do {
			return (try context.fetch(PlantArchitecture.fetchRequest())).count
		}
		catch  {
			print("Failed to load plants for collectionView: numberOfItemsInSection")
			return 0
		}
	}
	
	func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
		let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "PlantCell", for: indexPath) as! PlantCollectionViewCell
		
		let thisPlant = self.items?[indexPath.row]
		cell.plantLabel.text = thisPlant?.name
		
		// Rando color
		let randored = CGFloat.random(in: 0.0..<1.0)
		let randogreen = CGFloat.random(in: 0.0..<1.0)
		let randoblue = CGFloat.random(in: 0.0..<1.0)
		cell.backgroundColor = UIColor(cgColor: CGColor(srgbRed: randored, green: randogreen, blue: randoblue, alpha: 1.0))
		
		return cell
	}
}

extension ViewController: UICollectionViewDelegateFlowLayout {
	
	override func viewDidLayoutSubviews() {
		super.viewDidLayoutSubviews()
		
		flowLayout.scrollDirection = .vertical
		flowLayout.minimumLineSpacing = 10
		flowLayout.sectionInset = UIEdgeInsets(top: 10, left: 0, bottom: 10, right: 0)
	}
	
	func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
		let width = collectionView.bounds.width
		
		return CGSize(width: width, height: width / 2)
	}
}
