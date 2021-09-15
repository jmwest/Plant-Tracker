//
//  CalendarCollectionViewCell.swift
//  PlantTest
//
//  Created by John West on 11/11/20.
//  Copyright © 2020 John West. All rights reserved.
//

import UIKit
import JTAppleCalendar

class DateCell: JTACDayCell {
    
	@IBOutlet weak var dateCellLabel: UILabel!
	@IBOutlet weak var selectedCellView: UIView!
	@IBOutlet weak var rightRangeSelectedCellView: UIView!
	@IBOutlet weak var leftRangeSelectedCellView: UIView!
	@IBOutlet weak var eventTableView: UITableView!
	
}
