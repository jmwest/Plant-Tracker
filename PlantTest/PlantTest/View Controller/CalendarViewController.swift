//
//  CalendarViewController.swift
//  PlantTest
//
//  Created by John West on 11/10/20.
//  Copyright © 2020 John West. All rights reserved.
//

import UIKit
import JTAppleCalendar

class CalendarViewController: UIViewController {

	@IBOutlet weak var calendarMonthView: JTACMonthView!
	private var formatter = DateFormatter()
	
	// TestCalendar for dragging selection range
	let testCalendar = Calendar(identifier: .gregorian)
	
	override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
		let currentDate = Date()
		calendarMonthView.scrollToDate(currentDate, animateScroll: false)
		
		// Calendar scroll/page functionality
		calendarMonthView.scrollingMode = .stopAtEachCalendarFrame
		calendarMonthView.scrollDirection = .horizontal
		calendarMonthView.showsHorizontalScrollIndicator = false
		
		// Calendar multiple selections
		calendarMonthView.allowsMultipleSelection = true
		calendarMonthView.allowsRangedSelection = true
		
		// Calendar drag selection
		let panGesture = UILongPressGestureRecognizer(target: self,
													  action: #selector(didStartRangeSelecting(gesture:)))
		panGesture.minimumPressDuration = 0.5
		calendarMonthView.addGestureRecognizer(panGesture)
    }
	
	// Cell Select/Deselect Functions
	func calendar(_ calendar: JTACMonthView, didSelectDate date: Date, cell: JTACDayCell?, cellState: CellState, indexPath: IndexPath) {
		configureCell(view: cell, cellState: cellState)
	}
	
	func calendar(_ calendar: JTACMonthView, didDeselectDate date: Date, cell: JTACDayCell?, cellState: CellState, indexPath: IndexPath) {
		configureCell(view: cell, cellState: cellState)
	}
	
	//Header Delegates
	func calendar(_ calendar: JTACMonthView, headerViewForDateRange range: (start: Date, end: Date), at indexPath: IndexPath) -> JTACMonthReusableView {

		formatter.dateFormat = "MMM yyyy"
		
		let header = calendar.dequeueReusableJTAppleSupplementaryView(withReuseIdentifier: "DateHeader",
																	  for: indexPath) as! DateHeader
		
		header.monthYearTitle.text = formatter.string(from: range.start)
		
		return header
	}
	
	func calendarSizeForMonths(_ calendar: JTACMonthView?) -> MonthSize? {
		return MonthSize(defaultSize: 80)
	}
	
    // Congfiguring Calendar Cell
	func configureCell(view: JTACDayCell?, cellState: CellState) {
		
		guard let cell = view as? DateCell else {	return		}
		cell.dateCellLabel.text = cellState.text
		handleCellTextColor(cell: cell, cellState: cellState)
		handleCellSelected(cell: cell, cellState: cellState)
	}
	
	func handleCellTextColor(cell: DateCell, cellState: CellState) {
		
		if cellState.dateBelongsTo == .thisMonth {
			cell.dateCellLabel.textColor = UIColor.black
		}
		else {
			cell.dateCellLabel.textColor = UIColor.gray
		}
	}
	
	// Cell Highlighting Handler
	func handleCellSelected(cell: DateCell, cellState: CellState) {
		
		cell.selectedCellView.isHidden = !cellState.isSelected

		switch cellState.selectedPosition() {
		case .left:
			cell.selectedCellView.layer.cornerRadius = 15
			cell.selectedCellView.layer.maskedCorners = [.layerMinXMaxYCorner,
														 .layerMinXMinYCorner]
			
			cell.leftRangeSelectedCellView.isHidden = true
			cell.rightRangeSelectedCellView.isHidden = false

		case .middle:
			cell.selectedCellView.layer.cornerRadius = 0
			cell.selectedCellView.layer.maskedCorners = []

			cell.leftRangeSelectedCellView.isHidden = false
			cell.rightRangeSelectedCellView.isHidden = false
			
		case .right:
			cell.selectedCellView.layer.cornerRadius = 15
			cell.selectedCellView.layer.maskedCorners = [.layerMaxXMaxYCorner,
														 .layerMaxXMinYCorner]

			cell.leftRangeSelectedCellView.isHidden = false
			cell.rightRangeSelectedCellView.isHidden = true
			
		case .full:
			cell.selectedCellView.layer.cornerRadius = 15
			cell.selectedCellView.layer.maskedCorners = [.layerMaxXMaxYCorner,
														 .layerMaxXMinYCorner,
														 .layerMinXMaxYCorner,
														 .layerMinXMinYCorner]

			cell.leftRangeSelectedCellView.isHidden = true
			cell.rightRangeSelectedCellView.isHidden = true
			
		default:
			cell.leftRangeSelectedCellView.isHidden = true
			cell.rightRangeSelectedCellView.isHidden = true
			
			break
		}
	}
	
	// Function for dragging ranged selection
	@objc func didStartRangeSelecting(gesture: UILongPressGestureRecognizer) {
		
		let point = gesture.location(in: gesture.view!)
		let rangeSelectedDates = calendarMonthView.selectedDates
		
		guard let cellState = calendarMonthView.cellStatus(at: point) else { return }

		if !rangeSelectedDates.contains(cellState.date) {
			let dateRange = calendarMonthView.generateDateRange(from: rangeSelectedDates.first ?? cellState.date,
																to: cellState.date)
			calendarMonthView.selectDates(dateRange,
										  keepSelectionIfMultiSelectionAllowed: true)
		}
		else {
			let followingDay = testCalendar.date(byAdding: .day,
												 value: 1,
												 to: cellState.date)!
			calendarMonthView.selectDates(from: followingDay,
										  to: rangeSelectedDates.last!,
										  keepSelectionIfMultiSelectionAllowed: false)
		}
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

extension CalendarViewController: JTACMonthViewDataSource {

	func configureCalendar(_ calendar: JTACMonthView) -> ConfigurationParameters {

		formatter.dateFormat = "yyyy MM dd"
		
		let startDate = formatter.date(from: "2000 01 01")!
		let endDate = formatter.date(from: "2099 12 31")!
		
		return ConfigurationParameters(startDate: startDate,
									   endDate: endDate,
									   numberOfRows: 6,
									   generateInDates: .forAllMonths,
									   generateOutDates: .tillEndOfRow,
									   firstDayOfWeek: .sunday,
									   hasStrictBoundaries: true)
	}
}

extension CalendarViewController: JTACMonthViewDelegate {

	func calendar(_ calendar: JTACMonthView, cellForItemAt date: Date, cellState: CellState, indexPath: IndexPath) -> JTACDayCell {
		
		let cell = calendar.dequeueReusableJTAppleCell(withReuseIdentifier: "dateCell",
													   for: indexPath) as! DateCell
		
		self.calendar(calendar,
					  willDisplay: cell,
					  forItemAt: date,
					  cellState: cellState,
					  indexPath: indexPath)
		
		return cell
	}

	func calendar(_ calendar: JTACMonthView, willDisplay cell: JTACDayCell, forItemAt date: Date, cellState: CellState, indexPath: IndexPath) {
		
		configureCell(view: cell, cellState: cellState)
	}
	
	func calendar(_ calendar: JTACMonthView, willScrollToDateSegmentWith visibleDates: DateSegmentInfo) {
		
	}
}
