# Animation de Transition : Mode Sélection → Mode Entraînement

## 🎯 Objectif
Ajouter une animation fluide lors du passage du mode sélection au mode entraînement, déclenchée uniquement par le clic sur "Commencer l'entraînement".

## ✨ Effets Visuels

### Mode Sélection (Sortie)
- **Opacity** : 1 → 0
- **Transform** : translateY(0) → translateY(-20px)
- **Durée** : 350ms
- **Easing** : cubic-bezier(0.4, 0, 0.2, 1)

### Mode Entraînement (Entrée)
- **Opacity** : 0 → 1
- **Transform** : translateY(20px) → translateY(0) + scale(0.98) → scale(1)
- **Durée** : 350ms
- **Easing** : cubic-bezier(0.4, 0, 0.2, 1)

## 🛠️ Implémentation

### Classes CSS Ajoutées

#### `.selection-panel.exit` & `.control-panel.exit`
```css
.exit {
    opacity: 0;
    transform: translateY(-20px);
    pointer-events: none;
}
```

#### `.training-view.enter`, `.training-view.enter-active`, `.training-view.exit`
```css
.enter {
    opacity: 0;
    transform: translateY(20px) scale(0.98);
    pointer-events: none;
}

.enter-active {
    opacity: 1;
    transform: translateY(0) scale(1);
    pointer-events: auto;
}

.exit {
    opacity: 0;
    transform: translateY(20px) scale(0.98);
    pointer-events: none;
}
```

### Modifications JavaScript

#### `startTraining()`
1. Ajoute les classes `.exit` aux panneaux de sélection
2. Après 100ms : affiche la vue d'entraînement avec `.enter`
3. Déclenche l'animation avec `.enter-active`
4. Nettoie les classes après 350ms

#### `stopTraining()`
1. Ajoute la classe `.exit` à la vue d'entraînement
2. Après 100ms : affiche les panneaux de sélection
3. Retire les classes `.exit`
4. Masque complètement la vue d'entraînement après 350ms

## 🔧 Caractéristiques

- **Non-intrusif** : Aucune modification de la logique existante
- **Performance** : Utilise uniquement CSS transitions
- **Accessibilité** : `pointer-events: none` pendant les transitions
- **Fluidité** : Pas de clignotement ou de re-render brutal
- **Compatibilité** : Fonctionne avec le thème clair/sombre

## 🎨 Résultat

Une transition moderne, professionnelle et fluide qui améliore l'expérience utilisateur sans impacter le fonctionnement de l'application.
