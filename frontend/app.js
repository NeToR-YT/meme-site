document.addEventListener("DOMContentLoaded", () => {
    loadMemes();
    document.getElementById("meme-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const title = document.getElementById("title").value;
        const imageUrl = document.getElementById("image-url").value;
        const categoryId = parseInt(document.getElementById("category-id").value);

        await createMeme({ title, image_url: imageUrl, category_id: categoryId });
        loadMemes();
        document.getElementById("meme-form").reset();
    });
});

async function loadMemes() {
    const response = await fetch("http://localhost:8000/memes");
    const memes = await response.json();
    const gallery = document.getElementById("meme-gallery");
    gallery.innerHTML = "";
    memes.forEach(meme => {
        const div = document.createElement("div");
        div.className = "meme-item";
        div.innerHTML = `<h3>${meme.title}</h3><img src="${meme.image_url}" alt="${meme.title}"><p>Категорія: ${meme.category_id}</p>`;
        gallery.appendChild(div);
    });
}

async function createMeme(meme) {
    await fetch("http://localhost:8000/memes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(meme)
    });
}