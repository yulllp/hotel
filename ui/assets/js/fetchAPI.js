document.addEventListener('DOMContentLoaded', function () {
    async function fetchHotelData() {
        try {
            const response = await fetch('http://localhost:8000/merlynn_park_hotel', {
                method: "GET"
            }); // Adjust the URL as necessary
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            console.log(data);
            if (data) {
                const header = document.getElementById('header-background')
                header.style.backgroundImage = `url('${data.image}')`
                // Update About Us section
                const aboutUsContent = document.getElementById('about-us-content');
                aboutUsContent.innerHTML = `
                    <p>${data.description}</p>
                `;
                // Update Facilities section
                const facilitiesContent = document.getElementById('facilities-content');
                facilitiesContent.innerHTML = `
                    <p>${data.facilities}</p>
                `;
            } // Return the hotel data
        } catch (error) {
            console.error('Error fetching hotel data:', error);
            return null;
        }
    }

    fetchHotelData()
});

function getRoomType() {
    return {
        activeSlide: 1,
        slides: [],
        modalData: {},

        async fetchRoomType() {
            try {
                const response = await fetch('http://localhost:8000/merlynn_park_hotel/room_type', {
                    method: "GET"
                }); // Adjust the URL as necessary
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                const data = await response.json();
                console.log(data);
                this.slides = this.slides = data.map(room => ({
                    ...room,
                    price: `Rp ${room.price.toLocaleString('id-ID')}` // Format price with Indonesian locale
                }));
                console.log(this.slides)

            } catch (error) {
                console.error('Error fetching room type data:', error);
                return null;
            }
        },

        init() {
            this.fetchRoomType();
        }
    }
}