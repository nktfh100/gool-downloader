function timeToSeconds(timeString) {
	let parts = timeString.split(":");
	let hours = parseInt(parts[0], 10);
	let minutes = parseInt(parts[1], 10);
	let seconds = parseInt(parts[2], 10);
	return hours * 3600 + minutes * 60 + seconds;
}

let parentContainer = document.querySelector(
	".scrollobar_content.mCustomScrollbar"
);

let targetedNumbersBoxes = parentContainer.querySelectorAll(
	".targeted_numbers_box"
);

let allExtractedData = [];

targetedNumbersBoxes.forEach(function (targetedNumbersBox) {
	const title = targetedNumbersBox
		.querySelector(".targeted_number_title h2")
		.innerText.trim();

	const items = targetedNumbersBox.querySelectorAll(
		".targeted_number_check_box li"
	);

	let extractedData = [];

	let topicId = "";

	items.forEach(function (item) {
		topicId = item.getAttribute("data-topic-id");
		const videoId = item.getAttribute("data-video-id");
		const title = item.querySelector("span").innerText.trim();
		const videoLength = item.querySelector(".date_time").innerText.trim();

		if (!videoId) {
			return;
		}

		extractedData.push({
			title: title,
			videoId: videoId,
			videoLengthSeconds: timeToSeconds(videoLength),
		});
	});

	console.log(title);

	if (!topicId) {
		return;
	}

	allExtractedData.push({
		title: title,
		topicId: topicId,
		data: extractedData,
	});
});

console.log(JSON.stringify(allExtractedData));

return allExtractedData;
