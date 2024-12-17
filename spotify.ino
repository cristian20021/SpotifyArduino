#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9
#define SS_PIN          10

const int POTENTIOMETER = A0;   // Potentiometer connected to analog pin A0

MFRC522 mfrc522( SS_PIN, RST_PIN ); // Create MFRC522 instance

unsigned long       g_ulLastVolumeUpdate = 0;   // Track the last time volume was updated
const unsigned long g_ulVolumeInterval   = 500; // Update volume every 500 ms

void setup( void )
{
    Serial.begin( 115200 );
    // Wait for serial port to be ready
    while ( !Serial );
    SPI.begin();
    mfrc522.PCD_Init();
    Serial.println( "Place your MIFARE Ultralight card near the reader..." );
}

void handleVolume( void )
{
    static int c_iLastVolumeVal = -1;

    // Read the potentiometer value (0-1023) and map it to a percentage (0-100)
    int iPotentiometerValue = analogRead( POTENTIOMETER );
    int iVolume             = map( iPotentiometerValue, 0, 1023, 0, 100 );

    // Don't send volume data if it hasn't changed
    if ( c_iLastVolumeVal == iVolume )
    {
        return;
    }

    c_iLastVolumeVal = iVolume;

    Serial.print( "VOLUME:" );
    Serial.println( iVolume );
}

void loop( void )
{
    // Periodically send the volume value
    unsigned long ulCurrentTime = millis();
    if ( ( ulCurrentTime - g_ulLastVolumeUpdate ) >= g_ulVolumeInterval )
    {
        g_ulLastVolumeUpdate = ulCurrentTime;
        handleVolume();
    }

    // Look for new cards
    if ( !mfrc522.PICC_IsNewCardPresent() )
    {
        return;
    }

    // Select one of the cards
    if ( !mfrc522.PICC_ReadCardSerial() )
    {
        return;
    }

    // Get the type of the PICC
    MFRC522::PICC_Type PICCType = mfrc522.PICC_GetType( mfrc522.uid.sak );
    Serial.print( "Card Type: " );
    Serial.println( mfrc522.PICC_GetTypeName( PICCType ) );

    if ( PICCType == MFRC522::PICC_TYPE_MIFARE_UL )
    {
        // MIFARE Ultralight Card
        readAlbumURIData();
    }
    else
    {
        Serial.println( "Unsupported card type." );
    }

    // Halt PICC
    mfrc522.PICC_HaltA();
    // Stop encryption on PCD (if any)
    mfrc522.PCD_StopCrypto1();

    delay( 1000 );  // Prevent multiple reads
}

void readAlbumURIData( void )
{
    Serial.println( "Reading Spotify album URI data from card..." );

    const byte bStartPage = 4;   // Start reading from page 4 (user data)
    const byte bMaxPage   = 39;  // Maximum page number
    
    byte Buffer[ 18 ];
    byte cbBuffer = sizeof( Buffer );
    byte Data[ 128 ];
    int  iDataIndex = 0;
    bool fEndOfData = false;

    for ( byte bPage = bStartPage; bPage <= bMaxPage && !fEndOfData; bPage++ )
    {
        // Read one page at a time (4 bytes)
        MFRC522::StatusCode Status = mfrc522.MIFARE_Read( bPage, Buffer, &cbBuffer );

        if ( Status != MFRC522::STATUS_OK )
        {
            Serial.print( "Reading failed at page " );
            Serial.print( bPage );
            Serial.print( ": " );
            Serial.println( mfrc522.GetStatusCodeName( Status ) );
            break;
        }

        // Copy the data to our data buffer
        for ( byte i = 0; i < 4; i++ )
        {
            Data[ iDataIndex++ ] = Buffer[ i ];
            // Check for null terminator (end of string)
            if ( Buffer[ i ] == 0x00 )
            {
                fEndOfData = true;
                break;
            }
        }
    }

    // Send the album URI
    Serial.print( "Album URI:" );
    for ( int i = 0; i < iDataIndex; i++ )
    {
        Serial.write( Data[ i ] );  // Send as raw bytes to preserve the text
    }
    Serial.println();  // Newline for clarity
}
