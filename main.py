import streamlit as st
import random
import Musicians as mus

# Sayfa Yapılandırması
st.set_page_config(page_title="Song Blind Sort", page_icon="🎵")
st.title("🎵 Şarkı Blind Sort")

# Oyun Durumunu (Session State) Hazırlama
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.final_list = []
    st.session_state.musician_list = []
    st.session_state.song1 = ""
    st.session_state.song2 = ""

# --- GİRİŞ EKRANI ---
if not st.session_state.game_started:
    st.write("Hangi sanatçıyı sıralamak istersin?")
    secenekler = list(mus.musicians.keys())
    secilen = st.selectbox("Sanatçı Seç:", secenekler)
    
    if st.button("Sıralamaya Başla"):
        st.session_state.musician_list = mus.musicians[secilen].copy()
        if len(st.session_state.musician_list) < 2:
            st.error("Liste çok kısa!")
        else:
            # İlk seçimler
            st.session_state.song1 = st.session_state.musician_list.pop(random.randrange(len(st.session_state.musician_list)))
            st.session_state.song2 = st.session_state.musician_list.pop(random.randrange(len(st.session_state.musician_list)))
            st.session_state.game_started = True
            st.rerun()

# --- OYUN EKRANI ---
else:
    if st.session_state.song2: # Eğer hala karşılaştırılacak şarkı varsa
        st.write(f"### Hangi Şarkı Daha İyi?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(st.session_state.song1, use_container_width=True):
                # 1 Seçildi (Song1 kazandı, Song2 elendi)
                st.session_state.final_list.append(st.session_state.song2)
                if st.session_state.musician_list:
                    st.session_state.song2 = st.session_state.musician_list.pop(random.randrange(len(st.session_state.musician_list)))
                else:
                    st.session_state.song2 = ""
                st.rerun()

        with col2:
            if st.button(st.session_state.song2, use_container_width=True):
                # 2 Seçildi (Song2 kazandı, Song1 elendi)
                st.session_state.final_list.append(st.session_state.song1)
                st.session_state.song1 = st.session_state.song2
                if st.session_state.musician_list:
                    st.session_state.song2 = st.session_state.musician_list.pop(random.randrange(len(st.session_state.musician_list)))
                else:
                    st.session_state.song2 = ""
                st.rerun()

    # --- SONUÇ EKRANI ---
    else:
        st.success("Sıralama Tamamlandı!")
        st.session_state.final_list.append(st.session_state.song1)
        
        # Senin mantığında liste tersten basılıyordu
        son_liste = st.session_state.final_list[::-1]
        
        for i, song in enumerate(son_liste):
            st.write(f"**{i+1}.** {song}")
            
        if st.button("Yeniden Başla"):
            st.session_state.game_started = False
            st.rerun()