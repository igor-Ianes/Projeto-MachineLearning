import numpy as np
import librosa
import joblib
import os


def extrair_features(arquivo):

    y, sr = librosa.load(arquivo, duration=30)

    features = []

    # length
    features.append(len(y))

    # Chroma
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    features.extend([np.mean(chroma), np.var(chroma)])

    # RMS
    rms = librosa.feature.rms(y=y)
    features.extend([np.mean(rms), np.var(rms)])

    # Spectral Centroid
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    features.extend([np.mean(centroid), np.var(centroid)])

    # Spectral Bandwidth
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    features.extend([np.mean(bandwidth), np.var(bandwidth)])

    # Rolloff
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    features.extend([np.mean(rolloff), np.var(rolloff)])

    # Zero Crossing Rate
    zcr = librosa.feature.zero_crossing_rate(y)
    features.extend([np.mean(zcr), np.var(zcr)])

    # Harmony
    harmony = librosa.effects.harmonic(y)
    features.extend([np.mean(harmony), np.var(harmony)])

    # Percussive
    percussive = librosa.effects.percussive(y)
    features.extend([np.mean(percussive), np.var(percussive)])

    # Tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    features.append(float(np.asarray(tempo).item()))

    # MFCC
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)

    for coef in mfcc:
        features.extend([np.mean(coef), np.var(coef)])

    return np.array(features)

# ============================
# Carregar modelo
# ============================

modelo = joblib.load("modelo_random_forest.pkl")
scaler = joblib.load("scaler.pkl")
encoder = joblib.load("encoder.pkl")


def classificar():

    arquivo = input("\nDigite o caminho da música: ").strip()

    while not os.path.exists(arquivo):
        print("❌ Arquivo não encontrado!")
        arquivo = input("Digite novamente: ").strip()

    nome = os.path.basename(arquivo)

    print(f"\n🎵 Música: {nome}")

    features = extrair_features(arquivo)

    features = scaler.transform([features])

    pred = modelo.predict(features)

    prob = modelo.predict_proba(features)[0]

    genero = encoder.inverse_transform(pred)[0]

    confianca = np.max(prob)

    print("\n===========================")
    print(f"🎼 Gênero previsto: {genero}")
    print(f"📊 Confiança: {confianca*100:.2f}%")

    ranking = sorted(
        zip(encoder.classes_, prob),
        key=lambda x: x[1],
        reverse=True
    )

    print("\nRanking de probabilidades")
    print("-"*35)

    for i, (g, valor) in enumerate(ranking, start=1):
        print(f"{i:2d}° {g:10} {valor*100:6.2f}%")

print("="*50)
print("🎵 CLASSIFICADOR DE GÊNEROS MUSICAIS")
print("="*50)

while True:

    classificar()

    resposta = input("\nDeseja analisar outra música? (s/n): ").lower()

    if resposta != "s":
        break

print("\nPrograma encerrado!")