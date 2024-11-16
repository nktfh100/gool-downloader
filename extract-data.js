const isBagrut = window.location.href.toLowerCase().includes("bagrut");

let parentContainer = document.querySelector(
	isBagrut
		? ".scrollobar_content.mCustomScrollbar"
		: ".topics-list.list-unstyled.list-el-video"
);

let subjectsListContainer = isBagrut
	? parentContainer.querySelectorAll(".targeted_numbers_box")
	: Array.from(parentContainer.children).filter(
			(element) => element.tagName === "LI"
	  );

let allExtractedData = [];

subjectsListContainer.forEach(function (subjectContainer) {
	const title = isBagrut
		? subjectContainer
				.querySelector(".targeted_number_title h2")
				.innerText.trim()
		: subjectContainer.querySelector("u").innerText.trim();

	const items = isBagrut
		? subjectContainer.querySelectorAll(".targeted_number_check_box li")
		: subjectContainer.querySelectorAll("li");

	let extractedData = [];

	let topicId = "";

	items.forEach(function (item) {
		topicId = item.getAttribute("data-topic-id");
		const videoId = item.getAttribute("data-video-id");
		const title = isBagrut
			? item.querySelector("span").innerText.trim()
			: item.innerText.trim();

		if (!videoId) {
			return;
		}

		extractedData.push({
			title: title,
			videoId: videoId,
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
